from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def index(request):
    return redirect("/admin")


def get_user(request):
    print(request)

    return redirect("/admin")
