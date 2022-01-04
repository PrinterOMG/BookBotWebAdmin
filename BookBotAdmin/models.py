from django.db import models
import datetime


class Users(models.Model):
    userId = models.IntegerField(primary_key=True, verbose_name="")
    balance = models.DecimalField(default=0.0, verbose_name="")
    referral = models.ForeignKey("Users", default=None, null=True, on_delete=models.CASCADE, verbose_name="")
    isBlock = models.BooleanField(default=False, verbose_name="")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="")
    showProgress = models.BooleanField(default=False)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Promocodes(models.Model):
    promocodeId = models.BigAutoField(primary_key=True)
    promocode = models.CharField(max_length=64, verbose_name="")
    isUsed = models.BooleanField(default=False, verbose_name="")
    whoUsed = models.ForeignKey("Users", default=None, null=True)
    discount = models.IntegerField(verbose_name="")

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Questions(models.Model):
    questionId = models.BigAutoField(primary_key=True)
    text = models.TextField(verbose_name="")
    answer = models.TextField(default=None, null=True, verbose_name="")
    isAnswered = models.BooleanField(default=False, verbose_name="")

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Stats(models.Model):
    statsId = models.BigAutoField(primary_key=True)
    userId = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="")
    deposit = models.DecimalField(default=0.0, verbose_name="")
    subscribeTime = models.IntegerField(default=0, verbose_name="")

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Subscribes(models.Model):
    subscribeId = models.BigAutoField(primary_key=True)
    startDate = models.DateField(default=datetime.date.today(), verbose_name="")
    endDate = models.DateField(verbose_name="")
    isActive = models.BooleanField(default=True, verbose_name="")
    subPriceId = models.ForeignKey("SubPrices", on_delete=models.CASCADE, verbose_name="")

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Filters(models.Model):
    filterId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="")
    subscribeTime = models.IntegerField(default=0, verbose_name="")
    deposit = models.DecimalField(default=0.0, verbose_name="")
    balance = models.DecimalField(default=0.0, verbose_name="")
    isSubscribed = models.BooleanField(default=False, verbose_name="")

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Mailing(models.Model):
    mailingId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Posts(models.Model):
    postId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Books(models.Model):
    bookId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class SubPrices(models.Model):
    subPriceId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Languages(models.Model):
    languageId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class UsersAndBooks(models.Model):
    connectionId = models.BigAutoField(primary_key=True)

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""


class Settings(models.Model):
    text = models.TextField(verbose_name="")
    image = models.ImageField()

    def __repr__(self):
        return f""

    def __str__(self):
        return f""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
