from django.contrib import admin
from . import models


class UsersAdmin(admin.ModelAdmin):
    list_display = ("userId", "balance", "referral", "isBlock", "languageId", "showProgress")
    list_display_links = ["userId"]
    search_fields = ["userId"]
    # list_filter = ("balance", "referral", "isblock")


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]


class ReferralAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "registerCount"]


class SubPricesAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "duration"]


class PromocodesAdmin(admin.ModelAdmin):
    list_display = ["promocode"]


admin.site.register(models.Users, UsersAdmin)
admin.site.register(models.SubPrices, SubPricesAdmin)
admin.site.register(models.Filters)
admin.site.register(models.Mailing)
admin.site.register(models.Promocodes, PromocodesAdmin)
admin.site.register(models.Posts)
admin.site.register(models.Books)
admin.site.register(models.Languages, LanguagesAdmin)
admin.site.register(models.Subscribes)
admin.site.register(models.Questions)
admin.site.register(models.Referrals, ReferralAdmin)
