from django.db import models


class Users(models.Model):
    userId = models.IntegerField(primary_key=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=128, verbose_name="Имя пользователя")
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    referral = models.ForeignKey("Referrals", default=None, null=True, on_delete=models.CASCADE, verbose_name="Реферал", blank=True)
    isBlock = models.BooleanField(default=False, verbose_name="Заблокировал ли бота")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="Язык", blank=True)
    showProgress = models.BooleanField(default=False, verbose_name="Показывать ли прогресс сбора")
    deposit = models.IntegerField(default=0, verbose_name="Депозит")
    subscribeTime = models.IntegerField(default=0, verbose_name="Месяцы подписки")
    notEndPayment = models.BooleanField(verbose_name="Не закончил оплату")

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return "Тута скачивание данных о пользователе"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Promocodes(models.Model):
    promocodeId = models.BigAutoField(primary_key=True)
    promocode = models.CharField(max_length=64, verbose_name="Промокод", unique=True)
    isUsed = models.BooleanField(default=False, verbose_name="Использован ли")
    whoUsed = models.ForeignKey("Users", on_delete=models.CASCADE, default=None, null=True, verbose_name="Кто использовал", blank=True)
    discount = models.IntegerField(verbose_name="Скидка")
    subPriceId = models.ManyToManyField("SubPrices", null=True, verbose_name="На какие подписки")
    isActive = models.BooleanField(default=False, verbose_name="Активен ли")

    def __repr__(self):
        return self.promocode

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"


class Questions(models.Model):
    questionId = models.BigAutoField(primary_key=True)
    text = models.TextField(verbose_name="Текст")
    answer = models.TextField(default=None, null=True, verbose_name="Ответ")
    isAnswered = models.BooleanField(default=False, verbose_name="Отвечен ли")
    fromUser = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="От пользователя")

    def __repr__(self):
        return f"Вопрос №{self.pk}"

    def __str__(self):
        return f"Вопрос №{self.pk}"

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
    userId = models.ManyToManyField("Users", verbose_name="Заплатившие пользователи", blank=True, null=True)

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
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цена на подписку"
        verbose_name_plural = "Цены на подписки"


class Languages(models.Model):
    languageId = models.BigAutoField(primary_key=True)
    bookFile = models.FileField(verbose_name="", upload_to="static/books/")
    name = models.CharField(max_length=64, verbose_name="Название языка")
    backButton = models.CharField(max_length=64, verbose_name="Кнопка 'Назад'")
    okButton = models.CharField(max_length=64, verbose_name="Кнопка 'Ок'")
    cancelButton = models.CharField(max_length=64, verbose_name="Кнопка отмены")
    mainMenu = models.TextField(verbose_name="Текст в главном меню")
    changeLanguageButton = models.CharField(max_length=64, verbose_name="Кнопка смены яызка")
    subscribesButton = models.CharField(max_length=64, verbose_name="Кнопка перехода на покупку подписок")
    infoButton = models.CharField(max_length=64, verbose_name="Кнопка с информацией")
    fundraisingButton = models.CharField(max_length=64, verbose_name="Кнопка перехода на фандрайзинг")
    booksArchiveButton = models.CharField(max_length=64, verbose_name="Кнопка перехода на архив книг")
    makeQuestionButton = models.CharField(max_length=64, verbose_name="Кнопка 'Задать вопрос'")
    balanceButton = models.CharField(max_length=64, verbose_name="Кнопка 'Баланс'")
    changeLanguageOk = models.CharField(max_length=128, verbose_name="Уведомление об успешной смене языка")
    subscribesMenu = models.TextField(verbose_name="Меню покупки подписки")
    buySubButton = models.CharField(max_length=64, verbose_name="Кнопка покупки подписки ({duration} - срок, {price} - цена)")
    usePromocodeButton = models.CharField(max_length=64, verbose_name="Кнопка использования промокода")
    promoInput = models.TextField(verbose_name="Инструкция по введению промокода")
    cancelPromoButton = models.CharField(max_length=64, verbose_name="Кнопка для отмены активного промокода")
    cancelPromoOk = models.TextField(verbose_name="Уведомлении об успешной отмене активного промокода")
    promoNotExists = models.TextField(verbose_name="Ошибка отсутствия промокода")
    promoAlreadyUsed = models.TextField(verbose_name="Промокод уже использован")
    promoOk = models.TextField(verbose_name="Уведомление об успешной активации промокода ({code}, {discount})")
    info = models.TextField(verbose_name="Информация")
    balanceMenu = models.TextField(verbose_name="Меню баланса ({balance})")
    topUpButton = models.CharField(max_length=64, verbose_name="Кнопка для пополнения баланса")
    topUpInput = models.TextField(verbose_name="Инструкция по введению суммы пополнения")
    topUpError = models.TextField(verbose_name="Указана неверная сумма для пополнения")
    questionInput = models.TextField(verbose_name="Инструкция по введению вопроса")
    questionLimitError = models.TextField(verbose_name="Ошибка лимита символов ({limit})")
    questionOk = models.TextField(verbose_name="Уведомление об успешной отправке вопроса")
    answerText = models.TextField(verbose_name="Сообщение с ответом на вопрос ({question}, {answer})")
    paymentMenu = models.TextField(verbose_name="Меню выбора способа оплаты")
    telegramPayButton = models.CharField(max_length=64, verbose_name="Оплата через телеграм")
    yookassaButton = models.CharField(max_length=64, verbose_name="Оплата через ЮКассу")
    paypalButton = models.CharField(max_length=64, verbose_name="Оплата через PayPal")
    sbpButton = models.CharField(max_length=64, verbose_name="Оплата через СБП")
    booksArchiveMenu = models.TextField(verbose_name="Меню архива книг")
    yearButton = models.CharField(max_length=64, verbose_name="Поиск по году")
    genreButton = models.CharField(max_length=64, verbose_name="Поиск по жанру")
    authorButton = models.CharField(max_length=64, verbose_name="Поиск по автору")
    titleButton = models.CharField(max_length=64, verbose_name="Поиск по названию")
    searchInput = models.TextField(verbose_name="Инструкция по вводу поиска")
    searchError = models.TextField(verbose_name="Ничего не найдено")
    searchResult = models.TextField(verbose_name="Сообщение с результатом поиска ({books})")
    bookFormat = models.TextField(verbose_name="Формат вывода книги ({id}, {author}, {title}, {year}, {genre}, {price})")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


class Referrals(models.Model):
    referralId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="Название")
    code = models.CharField(max_length=128, verbose_name="Код")
    registerCount = models.IntegerField(default=0, verbose_name="Кол-во регистраций")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реферальный код"
        verbose_name_plural = "Реферальные коды"


class Settings(models.Model):
    name = models.CharField(max_length=64)
    questionSymbolsLimit = models.IntegerField(default=300, verbose_name="Лимит символов в вопросе (0 для отключения)")
    registerMenu = models.TextField(verbose_name="Меню выбора языка при регистрации")
    topUpLimit = models.IntegerField(default=10000, verbose_name="Лимит пополнения баланса")

    def __repr__(self):
        return "Настройки"

    def __str__(self):
        return "Настройки"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class Operations(models.Model):
    operationId = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="Пользователь")
    type = models.CharField(max_length=128, verbose_name="Тип")
    topUp = models.IntegerField(blank=True, null=True, verbose_name="Сумма пополнения")
    bookFund = models.ForeignKey("Books", on_delete=models.CASCADE, verbose_name="Книга из фандрайзинга", blank=True, null=True)
    bookArchive = models.IntegerField(blank=True, null=True, verbose_name="Книга из архива")
    subscribe = models.ForeignKey("SubPrices", on_delete=models.CASCADE, verbose_name="Подписка")
    paymentMethod = models.CharField(max_length=128, verbose_name="Способ оплаты", blank=True, null=True)
