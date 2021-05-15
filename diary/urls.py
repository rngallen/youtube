from . import views
from django.urls import path

app_name = "diary"

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
]
