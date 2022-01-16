from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models as md
from . import models


class UsersAdmin(admin.ModelAdmin):
    list_display = ("userId", "username", "balance", "referral", "isBlock", "languageId", "showProgress")
    list_display_links = ["userId", "username"]
    search_fields = ["userId", "username"]
    list_filter = ("balance", "referral", "isBlock")
    fields = ("userId", "username", "balance", "deposit", "subscribeTime", "referral", "isBlock", "languageId", "showProgress", "notEndPayment")
    readonly_fields = ("userId", "username", "referral", "isBlock", "languageId", "showProgress", "notEndPayment", "subscribeTime")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]


class ReferralAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "registerCount"]


class SubPricesAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "duration"]


class PromocodesAdmin(admin.ModelAdmin):
    list_display = ["promocode", "isUsed", "isActive", "whoUsed", "discount"]
    fields = ("promocode", "isUsed", "isActive", "whoUsed", "discount", "subPriceId")
    readonly_fields = ("isUsed", "whoUsed", "isActive")
    formfield_overrides = {
        md.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class SubscribesAdmin(admin.ModelAdmin):
    list_display = ["user", "endDate", "isActive"]
    fields = ["user", "startDate", "endDate", "subPriceId", "isActive"]
    readonly_fields = ["startDate", "endDate", "isActive", "user", "subPriceId"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SettingsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["questionSymbolsLimit", "registerMenu", "topUpLimit"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BooksAdmin(admin.ModelAdmin):
    list_display = ["name", "goalSum", "collectedSum", "isDone"]
    fields = ["name", "description", "startDate", "endDate", "goalSum", "collectedSum", "link", "isDone", "priceAfterDone", "priceForSub", "priceCommon", "userId"]
    readonly_fields = ["collectedSum", "isDone", "userId"]


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["fromUser"]
    fields = ["text", "answer", "isAnswered", "fromUser"]
    readonly_fields = ["text", "isAnswered", "fromUser"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Users, UsersAdmin)
admin.site.register(models.SubPrices, SubPricesAdmin)
admin.site.register(models.Filters)
admin.site.register(models.Mailing)
admin.site.register(models.Promocodes, PromocodesAdmin)
admin.site.register(models.Posts)
admin.site.register(models.Books, BooksAdmin)
admin.site.register(models.Languages, LanguagesAdmin)
admin.site.register(models.Subscribes, SubscribesAdmin)
admin.site.register(models.Questions, QuestionsAdmin)
admin.site.register(models.Referrals, ReferralAdmin)
admin.site.register(models.Settings, SettingsAdmin)
