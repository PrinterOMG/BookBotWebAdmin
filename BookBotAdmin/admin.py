from django.contrib import admin
from . import models


class UsersAdmin(admin.ModelAdmin):
    list_display = ("userId", "balance", "referral", "isBlock", "languageId", "showProgress")
    list_display_links = ["userId"]
    search_fields = ["userId"]
    # list_filter = ("balance", "referral", "isblock")


admin.site.register(models.Users, UsersAdmin)
admin.site.register(models.Stats)
admin.site.register(models.SubPrices)
admin.site.register(models.Settings)
admin.site.register(models.Filters)
admin.site.register(models.Mailing)
admin.site.register(models.Promocodes)
admin.site.register(models.Posts)
admin.site.register(models.Books)
admin.site.register(models.Languages)
admin.site.register(models.Subscribes)
admin.site.register(models.Questions)
