from django.shortcuts import render, redirect
from .models import Users, Subscribes
from django.http import FileResponse

import pandas as pd


def index(request):
    return redirect("/admin")


def get_user(request, user_id):
    user = Users.objects.get(pk=user_id)
    print(user)

    data = {
        "Telegram ID": [user.pk],
        "Username": [user.username],
        "Balance": [user.balance],
        "Deposit": [user.deposit],
        "Referral": [user.referral],
        "Language": [user.languageId],
        "Subscribe time": [user.subscribeTime],
        "Not end payment": [user.notEndPayment],
        "Auto payment": [user.isAutoPay]
    }

    filename = f"static/users/{user_id}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name="User")

    return FileResponse(open(filename, "rb"))
    # return redirect(f"/admin/BookBotAdmin/users/{user_id}/change/")
