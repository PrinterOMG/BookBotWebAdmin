from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models as md
from . import models


@admin.register(models.Users)
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


@admin.register(models.Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]

    save_on_top = True


@admin.register(models.Referrals)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "registerCount"]
    fields = ["name", "code", "registerCount"]
    readonly_fields = ["registerCount"]


@admin.register(models.SubPrices)
class SubPricesAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "duration"]


@admin.register(models.Promocodes)
class PromocodesAdmin(admin.ModelAdmin):
    list_display = ["promocode", "isUsed", "isActive", "whoUsed", "discount"]
    fields = ("promocode", "isUsed", "isActive", "whoUsed", "discount", "subPriceId")
    readonly_fields = ("isUsed", "whoUsed", "isActive")
    formfield_overrides = {
        md.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(models.Subscribes)
class SubscribesAdmin(admin.ModelAdmin):
    list_display = ["user", "endDate", "isActive"]
    fields = ["user", "startDate", "endDate", "subPriceId", "isActive"]
    readonly_fields = ["startDate", "endDate", "isActive", "user", "subPriceId"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["questionSymbolsLimit", "registerMenu", "topUpLimit"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ["name", "startDate", "endDate", "goalSum", "collectedSum", "isDone"]
    fields = ["name", "description", "startDate", "endDate", "goalSum", "collectedSum", "link", "isDone", "priceAfterDone", "priceForSub", "priceCommon", "userId"]
    readonly_fields = ["collectedSum", "isDone", "userId"]


@admin.register(models.Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["text", "fromUser", "isAnswered", "date"]
    fields = ["text", "answer", "isAnswered", "fromUser"]
    readonly_fields = ["text", "isAnswered", "fromUser"]
    list_filter = ["isAnswered", "fromUser"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Filters)
class FiltersAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ["title", "isSend", "date"]
    fields = ["title", "text", "photo", "date", "filter", "isSend"]
    readonly_fields = ["date", "isSend"]


@admin.register(models.Statistic)
class Statistic(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "statisticId", "allSubsCounter", "noBuyUsersCounter", "blockUsersCounter", "interruptedPaymentsCount", "archiveBooksSum", "archiveBooksCount"]

    readonly_fields = ["statisticId", "allSubsCounter", "noBuyUsersCounter", "blockUsersCounter", "interruptedPaymentsCount", "archiveBooksSum", "archiveBooksCount"]

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

# admin.site.register(models.Mailing)
