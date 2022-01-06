from django.db import models


class Users(models.Model):
    userId = models.IntegerField(primary_key=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=128, verbose_name="Имя пользователя")
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    referral = models.ForeignKey("Users", default=None, null=True, on_delete=models.CASCADE, verbose_name="Реферал", blank=True)
    isBlock = models.BooleanField(default=False, verbose_name="Заблокировал ли бота")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="Язык", blank=True)
    showProgress = models.BooleanField(default=False, verbose_name="Показывать ли прогресс сбора")
    deposit = models.IntegerField(default=0, verbose_name="Депозит")
    subscribeTime = models.IntegerField(default=0, verbose_name="Месяцы подписки")

    def __repr__(self):
        return f"Пользователь"

    def __str__(self):
        return f""

    def get_absolute_url(self):
        return "Тута скачивание данных о пользователе"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Promocodes(models.Model):
    promocodeId = models.BigAutoField(primary_key=True)
    promocode = models.CharField(max_length=64, verbose_name="Промокод")
    isUsed = models.BooleanField(default=False, verbose_name="Использован ли")
    whoUsed = models.ForeignKey("Users", on_delete=models.CASCADE, default=None, null=True, verbose_name="Кто использовал")
    discount = models.IntegerField(verbose_name="Скидка")

    def __repr__(self):
        return f"Промокод"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"


class Questions(models.Model):
    questionId = models.BigAutoField(primary_key=True)
    text = models.TextField(verbose_name="Текст")
    answer = models.TextField(default=None, null=True, verbose_name="Ответ")
    isAnswered = models.BooleanField(default=False, verbose_name="Отвечен ли")

    def __repr__(self):
        return f"Вопрос"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Subscribes(models.Model):
    subscribeId = models.BigAutoField(primary_key=True)
    startDate = models.DateField(auto_now_add=True, verbose_name="Дата начала")
    endDate = models.DateField(verbose_name="Дата конца")
    isActive = models.BooleanField(default=True, verbose_name="Активна ли")
    subPriceId = models.ForeignKey("SubPrices", on_delete=models.CASCADE, verbose_name="Подписка")

    def __repr__(self):
        return f"Подписка"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Filters(models.Model):
    filterId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="Название")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="Язык")
    subscribeTime = models.IntegerField(default=0, verbose_name="Месяцы подписки")
    deposit = models.IntegerField(default=0, verbose_name="Депозит")
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    isSubscribed = models.BooleanField(default=False, verbose_name="Подписан ли")

    def __repr__(self):
        return f"Фильтр"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"


class Mailing(models.Model):
    mailingId = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    photo = models.ImageField(upload_to="imgs/mailing/", verbose_name="Картинка")
    date = models.DateTimeField(verbose_name="Дата")
    filter = models.ForeignKey("Filters", on_delete=models.CASCADE, verbose_name="Фильтр")

    def __repr__(self):
        return f"Рассылка"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Posts(models.Model):
    postId = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    photo = models.ImageField(upload_to="imgs/posts/", verbose_name="Картинка")
    date = models.DateTimeField(verbose_name="Дата")
    filter = models.ForeignKey("Filters", on_delete=models.CASCADE, verbose_name="Фильтр")

    def __repr__(self):
        return f"Пост"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Books(models.Model):
    bookId = models.BigAutoField(primary_key=True)
    description = models.TextField(verbose_name="Описание")
    startDate = models.DateField(verbose_name="Дата начала")
    endDate = models.DateField(verbose_name="Дата конца")
    goalSum = models.IntegerField(verbose_name="Необходимая сумма")
    collectedSum = models.IntegerField(verbose_name="Собранная сумма")
    link = models.CharField(max_length=64, verbose_name="Ссылка")
    isDone = models.BooleanField(default=False, verbose_name="Собрано ли")
    priceAfterDone = models.IntegerField(verbose_name="Цена после сбора")
    priceForSub = models.IntegerField(verbose_name="Цена для подписчика")
    priceCommon = models.IntegerField(verbose_name="Цена для всех")

    def __repr__(self):
        return f"Книга"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class SubPrices(models.Model):
    subPriceId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="Название")
    value = models.IntegerField(verbose_name="Цена")
    duration = models.IntegerField(verbose_name="Месяцы")

    def __repr__(self):
        return f"Цена на подписку"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Цена на подписку"
        verbose_name_plural = "Цены на подписки"


class Languages(models.Model):
    languageId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="")
    # backButton = models.CharField(max_length=64, verbose_name="")
    # mainMenu = models.TextField(verbose_name="")
    # infoButton = models.CharField(max_length=64, verbose_name="")
    # archiveButton = models.CharField(max_length=64, verbose_name="")
    # balanceButton = models.CharField(max_length=64, verbose_name="")
    # fundraisingButton = models.CharField(max_length=64, verbose_name="")
    # subscribeButton = models.CharField(max_length=64, verbose_name="")
    # makeQuestionButton = models.CharField(max_length=64, verbose_name="")
    # changeLanButton = models.CharField(max_length=64, verbose_name="")
    # subscribeMenu = models.TextField(verbose_name="")
    # buySubscribeButton = models.CharField(max_length=64, verbose_name="")
    # promocodeButton = models.CharField(max_length=64, verbose_name="")
    # promocodeErrot = models.TextField(verbose_name="")
    # promocodeOk = models.TextField(verbose_name="")
    # paymentMethod = models.TextField(verbose_name="")
    # infoText = models.TextField(verbose_name="")
    # bookBuyMenu = models.TextField(verbose_name="")
    # booksList = models.TextField(verbose_name="")
    # bookInfo = models.TextField(verbose_name="")
    # downloadBookButton = models.CharField(max_length=64, verbose_name="")
    # downloadError = models.TextField(verbose_name="")
    # downloadOk = models.TextField(verbose_name="")
    # buyButton = models.CharField(max_length=64, verbose_name="")

    def __repr__(self):
        return f"Язык"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


#  НЕ НУЖНО ОТОБРАЖАТЬ
class UsersAndBooks(models.Model):
    connectionId = models.BigAutoField(primary_key=True)
    userId = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="Пользователь")
    bookId = models.ForeignKey("Books", on_delete=models.CASCADE, verbose_name="Книга")

    def __repr__(self):
        return f"Связь"

    def __str__(self):
        return f""

    class Meta:
        verbose_name = "Связь"
        verbose_name_plural = "Связи"
#  НЕ НУЖНО ОТОБРАЖАТЬ


class Settings(models.Model):
    text = models.TextField(verbose_name="Текст для кнопки 2")

    def __repr__(self):
        return f"Настройки"

    def __str__(self):
        return f"Настройки"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
