from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def index(request):
    reverse("/admin")
