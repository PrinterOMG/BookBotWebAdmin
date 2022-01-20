from django.shortcuts import render, redirect
from .models import *
from django.http import FileResponse

import pandas as pd


def index(request):
    return redirect("/admin")


def get_user(request, user_id):
    user = Users.objects.get(pk=user_id)

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
    df.to_excel(filename, sheet_name="User", index=False)

    return FileResponse(open(filename, "rb"))
    # return redirect(f"/admin/BookBotAdmin/users/{user_id}/change/")


def get_stats(request):
    users_data = {
        "Telegram ID": [],
        "Username": [],
        "Balance": [],
        "Deposit": [],
        "Referral": [],
        "Language": [],
        "Subscribe time": [],
        "Not end payment": [],
        "Auto payment": [],
        "Is subscriber": [],
        "Subscribe end": []
    }
    for user in Users.objects.all():
        users_data["Telegram ID"].append(user.pk)
        users_data["Username"].append(user.username)
        users_data["Balance"].append(user.balance)
        users_data["Deposit"].append(user.deposit)
        users_data["Referral"].append(user.referral)
        users_data["Language"].append(user.languageId)
        users_data["Subscribe time"].append(user.subscribeTime)
        users_data["Not end payment"].append(user.notEndPayment)
        users_data["Auto payment"].append(user.isAutoPay)

        try:
            subscribe = Subscribes.objects.get(user_id=user.pk)
            users_data["Is subscriber"].append(subscribe.isActive)
            users_data["Subscribe end"].append(subscribe.endDate)
            print("Ok")
        except:
            users_data["Is subscriber"].append(False)
            users_data["Subscribe end"].append("0")

    referrals_data = {
        "Name": [],
        "Code": [],
        "Registrations count": []
    }
    for referral in Referrals.objects.all():
        referrals_data["Name"].append(referral.name)
        referrals_data["Code"].append(referral.code)
        referrals_data["Registrations count"].append(referral.registerCount)

    subscribes_data = {
        "Name": [],
        "Price": [],
        "Duration": [],
        "Active subscribes count": []
    }
    for subscribe in SubPrices.objects.all():
        subscribes_data["Name"].append(subscribe.name)
        subscribes_data["Price"].append(subscribe.value)
        subscribes_data["Duration"].append(subscribe.duration)

        active_subs_count = Subscribes.objects.all().filter(subPriceId_id=subscribe.pk, isActive=True).count()
        subscribes_data["Active subscribes count"].append(active_subs_count)

    stats = Statistic.objects.get(pk=3)
    statistics_data = {
        "All subscribers count": [stats.allSubsCounter],
        "No buy users count": [stats.noBuyUsersCounter],
        "Block users count": [stats.blockUsersCounter],
        "Interrupted payments count": [stats.interruptedPaymentsCount],
        "Archive books sum": [stats.archiveBooksSum],
        "Archive books count": [stats.archiveBooksCount]
    }

    fundraising_data = {
        "Name": [],
        "Buy users count": [],
        "Collected sum": [],
        "Progress": []
    }
    for book in Books.objects.all():
        fundraising_data["Name"].append(book.name)
        fundraising_data["Collected sum"].append(book.collectedSum)

        buy_users_count = book.userId.all().count()
        fundraising_data["Buy users count"].append(buy_users_count)

        progress = "100%" if book["collectedSum"] > book["goalSum"] else f"{round((book['collectedSum'] / book['goalSum']) * 100)}%"
        fundraising_data["Progress"].append(progress)

    file_path = r"static/stats.xlsx"
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    pd.DataFrame(users_data).to_excel(writer, sheet_name="Users", index=False)
    pd.DataFrame(fundraising_data).to_excel(writer, sheet_name="Fundraising", index=False)
    pd.DataFrame(subscribes_data).to_excel(writer, sheet_name="Subscribes", index=False)
    pd.DataFrame(referrals_data).to_excel(writer, sheet_name="Referrals", index=False)
    pd.DataFrame(statistics_data).to_excel(writer, sheet_name="Statistics", index=False)

    writer.save()
    writer.close()

    return FileResponse(open(file_path, "rb"))
