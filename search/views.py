from django.conf import settings
from django.shortcuts import render, redirect
import requests
from requests.exceptions import HTTPError
from .models import HttpError, ExceptionError, SuccessRequest
from isodate import parse_duration


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def home(request):
    ip_address = get_client_ip(request)
    videos = []
    if request.method == "POST":
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": settings.YOUTUBE_DATA_API_KEY,
            "part": "snippet",
            "maxResults": 9,
            "q": request.POST["search"],
            "type": "video",
        }
        try:
            videos, videos_ids = [], []
            results = requests.get(search_url, params=params)
            r = results.json()["items"]

            for video in r:
                video_id = video["id"]["videoId"]
                videos_ids.append(video_id)
            if request.POST["submit"] == "lucky":
                return redirect(f"https://www.youtube.com/watch?v={videos_ids[0]}")

            video_url = "https://www.googleapis.com/youtube/v3/videos"
            video_params = {
                "key": settings.YOUTUBE_DATA_API_KEY,
                "part": "snippet,contentDetails",
                "id": ",".join(videos_ids),
            }
            video_detail = requests.get(video_url, params=video_params)
            vr = video_detail.json()["items"]
            for i in vr:
                content = {
                    "duration": int(
                        parse_duration(i["contentDetails"]["duration"]).total_seconds()
                        // 60
                    ),
                    "channel": i["snippet"]["channelTitle"],
                    "thumbnail": i["snippet"]["thumbnails"]["maxres"]["url"],
                    "title": i["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={i['id']}",
                }
                videos.append(content)

        except HTTPError as http_err:
            http_error = f"HTTP error occured: {http_err}"
            error = HttpError(error_message=http_error, ip_address=ip_address)
            error.save()
        except Exception as err:
            exception_error = f"Other error occured {err}"
            new_error = ExceptionError(
                error_message=exception_error, ip_address=ip_address
            )
            new_error.save()
        else:
            success_msg = SuccessRequest(
                success_message=f"Request was Successfully",
                ip_address=ip_address,
                search=request.POST["search"],
            )
            success_msg.save()
    context = {
        "videos": videos,
    }
    return render(request, "search/index.html", context)


def customer_details(request):
    respiratories_list = []
    if request.method == "POST":
        CustomerNumber = "10001"
        for url in [
            f"http://localhost/Sage300WebApi/V1.0/-/FADAT/AR/ARCustomers('{CustomerNumber}')"
        ]:
            params = {
                # 'q': request.POST['search'],
            }
            with requests.Session() as session:
                try:
                    session.auth = (settings.SAGE_API_USER, settings.SAGE_API_PASSWORD)
                    response = session.get(
                        url,
                        params=params,
                    )
                    json_reponse = response.json()
                    print(json_reponse, response.headers)
                    respiratories = json_reponse["items"]
                    # if the response was successful, no Exception will be raised
                    response.raise_for_status()
                    # response.encoding = 'utf-8'
                except HTTPError as http_err:
                    print(f"HTTP error occured: {http_err}")
                except Exception as err:
                    print(f"Other error occured {err}")
                else:
                    print("Success!", url)
                    for respiratory in respiratories:
                        result = {
                            "id": respiratory["id"],
                            "name": respiratory["name"],
                            "full_name": respiratory["full_name"],
                            "channel": respiratory["owner"]["login"],
                            "thumbnail": respiratory["owner"]["avatar_url"],
                            "url": respiratory["owner"]["html_url"],
                            "title": respiratory["description"],
                            "duration": respiratory["forks_count"],
                        }
                        respiratories_list.append(result)
                    # print(response.headers)
    context = {
        "videos": respiratories_list,
    }
    return render(request, "search/index.html", context)
