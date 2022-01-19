from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def index(request):
    return redirect("/admin")
