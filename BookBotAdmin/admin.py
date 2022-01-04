from django.contrib import admin
from . import models


class UsersAdmin(admin.ModelAdmin):
    list_display = ("userId", "balance", "referral", "isBlock", "languageId", "showProgress")
    list_display_links = ["userId"]
    search_fields = ["userId"]
    # list_filter = ("balance", "referral", "isblock")


admin.site.register(models.Users, UsersAdmin)
