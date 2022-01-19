from django.shortcuts import render, redirect
from models import Users

# Create your views here.
from django.urls import reverse


def index(request):
    return redirect("/admin")


def get_user(request, user_id):
    user = Users.objects.get(pk=user_id)
    print(user)

    return redirect(f"/admin/BookBotAdmin/users/{user_id}/change/")
