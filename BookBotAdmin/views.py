from django.shortcuts import render, redirect
from .models import *
from django.http import FileResponse

import pandas as pd


def index(request):
    return redirect("/admin")


def get_user(request, user_id):
    user = Users.objects.get(pk=user_id)

    data = {
        "ID в Телеграмме": [user.pk],
        "Имя": [user.username],
        "Обращение": [user.mention],
        "Баланс": [user.balance],
        "Депозит": [user.deposit],
        "Реферал": [user.referral],
        "Язык": [user.languageId],
        "Время подписки": [user.subscribeTime],
        "Не закончил оплату": [user.notEndPayment],
        "Автоплатёж": [user.isAutoPay]
    }

    filename = f"static/users/{user_id}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name="User", index=False)

    return FileResponse(open(filename, "rb"))
    # return redirect(f"/admin/BookBotAdmin/users/{user_id}/change/")


def get_stats(request):
    users_data = {
        "ID в Телеграмме": [],
        "Имя": [],
        "Обращение": [],
        "Баланс": [],
        "Депозит": [],
        "Реферал": [],
        "Язык": [],
        "Время подписки": [],
        "Не закончил оплату": [],
        "Автоплатёж": [],
        "Подписан ли": [],
        "Дата конца подписки": [],
        "Срок подписки": [],
        "Цена подписки": []
    }
    for user in Users.objects.all():
        users_data["ID в Телеграмме"].append(user.pk)
        users_data["Имя"].append(user.username)
        users_data["Обращение"].append(user.mention)
        users_data["Баланс"].append(user.balance)
        users_data["Депозит"].append(user.deposit)
        users_data["Реферал"].append(user.referral)
        users_data["Язык"].append(user.languageId)
        users_data["Время подписки"].append(user.subscribeTime)
        users_data["Не закончил оплату"].append(user.notEndPayment)
        users_data["Автоплатёж"].append(user.isAutoPay)

        try:
            subscribe = Subscribes.objects.get(user_id=user.pk)
            users_data["Подписан ли"].append(subscribe.isActive)
            users_data["Дата конца подписки"].append(subscribe.endDate)

            subprice = SubPrices.objects.get(subPriceId=subscribe.subPriceId_id)
            users_data["Срок подписки"].append(subprice.duration)
            users_data["Цена подписки"].append(subprice.value)
        except:
            users_data["Подписан ли"].append(False)
            users_data["Дата конца подписки"].append("0")
            users_data["Срок подписки"].append("0")
            users_data["Цена подписки"].append("0")

    referrals_data = {
        "Название": [],
        "Код": [],
        "Кол-во регистраций": []
    }
    for referral in Referrals.objects.all():
        referrals_data["Название"].append(referral.name)
        referrals_data["Код"].append(referral.code)
        referrals_data["Кол-во регистраций"].append(referral.registerCount)

    subscribes_data = {
        "Название": [],
        "Цена": [],
        "Срок": [],
        "Кол-во подписчиков": []
    }
    for subscribe in SubPrices.objects.all():
        subscribes_data["Название"].append(subscribe.name)
        subscribes_data["Цена"].append(subscribe.value)
        subscribes_data["Срок"].append(subscribe.duration)

        active_subs_count = Subscribes.objects.all().filter(subPriceId_id=subscribe.pk, isActive=True).count()
        subscribes_data["Кол-во подписчиков"].append(active_subs_count)

    stats = Statistic.objects.get(pk=3)
    statistics_data = {
        "Кол-во пользователей с подпиской": [stats.allSubsCounter],
        "Кол-во пользователей без подписки": [stats.noBuyUsersCounter],
        "Кол-во пользователей заблокировавших бота": [stats.blockUsersCounter],
        "Кол-во незавершённых оплат": [stats.interruptedPaymentsCount],
        "Сумма собранных средств с книг из архива": [stats.archiveBooksSum],
        "Кол-во проданных книг из архива": [stats.archiveBooksCount]
    }

    fundraising_data = {
        "Название": [],
        "Кол-во купивших пользователей": [],
        "Собранная сумма": [],
        "Прогресс": []
    }
    for book in Books.objects.all():
        fundraising_data["Название"].append(book.name)
        fundraising_data["Собранная сумма"].append(book.collectedSum)

        buy_users_count = book.userId.all().count()
        fundraising_data["Кол-во купивших пользователей"].append(buy_users_count)

        progress = "100%" if book.collectedSum > book.goalSum else f"{round((book.collectedSum / book.goalSum) * 100)}%"
        fundraising_data["Прогресс"].append(progress)

    file_path = r"static/stats.xlsx"
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    pd.DataFrame(users_data).to_excel(writer, sheet_name="Пользователи", index=False)
    pd.DataFrame(fundraising_data).to_excel(writer, sheet_name="Фандрайзинг", index=False)
    pd.DataFrame(subscribes_data).to_excel(writer, sheet_name="Подписки", index=False)
    pd.DataFrame(referrals_data).to_excel(writer, sheet_name="Реферальные коды", index=False)
    pd.DataFrame(statistics_data).to_excel(writer, sheet_name="Статистика", index=False)

    writer.save()
    writer.close()

    return FileResponse(open(file_path, "rb"))
