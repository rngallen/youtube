from django.shortcuts import render, redirect
from .forms import EntryForm
from .models import Entry

# Create your views here.


def home(request):
    entries = Entry.objects.all()
    context = {
        "entries": entries,
    }
    return render(request, "diary/index.html", context)


def add(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("diary:home")
    context = {"form": EntryForm()}
    return render(request, "diary/add.html", context)
