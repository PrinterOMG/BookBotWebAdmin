import datetime

import django
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.urls import reverse


class Users(models.Model):
    userId = models.BigIntegerField(primary_key=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=128, verbose_name="Имя пользователя")
    mention = models.CharField(max_length=128, verbose_name="Обращение")
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    referral = models.ForeignKey("Referrals", default=None, null=True, on_delete=models.CASCADE, verbose_name="Реферал", blank=True)
    isBlock = models.BooleanField(default=False, verbose_name="Заблокировал ли бота")
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="Язык", blank=True)
    showProgress = models.BooleanField(default=False, verbose_name="Показывать ли прогресс сбора")
    deposit = models.IntegerField(default=0, verbose_name="Депозит")
    subscribeTime = models.IntegerField(default=0, verbose_name="Месяцы подписки")
    notEndPayment = models.BooleanField(verbose_name="Не закончил оплату")
    paymentId = models.CharField(max_length=128, verbose_name="Сохраненный способ оплаты", blank=True, null=True)
    isAutoPay = models.BooleanField(default=True, verbose_name="Автоплатеж")
    lastMenu = models.IntegerField(default=0)
    subscribeStatus = models.ForeignKey("SubscribeStatus", on_delete=models.CASCADE, default=1)
    buyBooks = models.TextField()
    isPaying = models.BooleanField(default=0, verbose_name="Индикатор состояния оплаты")

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("get_user", kwargs={"user_id": int(self.pk)})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Promocodes(models.Model):
    promocodeId = models.BigAutoField(primary_key=True)
    promocode = models.CharField(max_length=64, verbose_name="Промокод", unique=True)
    isUsed = models.BooleanField(default=False, verbose_name="Использован ли")
    whoUsed = models.ForeignKey("Users", on_delete=models.CASCADE, default=None, null=True, verbose_name="Кто использовал", blank=True)
    discount = models.IntegerField(verbose_name="Скидка")
    subPriceId = models.ManyToManyField("SubPrices", verbose_name="На какие подписки")
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
    date = models.DateTimeField(verbose_name="Дата вопроса", auto_created=True, auto_now=True)

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
    user = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="Пользователь")

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
    languageId = models.ForeignKey("Languages", on_delete=models.CASCADE, verbose_name="Язык", blank=True, null=True)
    subscribeTimeFrom = models.IntegerField(default=0, verbose_name="Месяцы подписки (От)")
    subscribeTimeTo = models.IntegerField(default=0, verbose_name="Месяцы подписки (До)")
    depositFrom = models.IntegerField(default=0, verbose_name="Депозит (От)")
    depositTo = models.IntegerField(default=0, verbose_name="Депозит (До)")
    balanceFrom = models.IntegerField(default=0, verbose_name="Баланс (От)")
    balanceTo = models.IntegerField(default=0, verbose_name="Баланс (До)")
    subscribeStatus = models.ForeignKey("SubscribeStatus", on_delete=models.CASCADE, verbose_name="Статус подписки", blank=True, null=True, default=None)
    notEndPayment = models.ForeignKey("PaymentStatus", on_delete=models.CASCADE, verbose_name="Статус оплаты", default=3)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"


class SubscribeStatus(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Posts(models.Model):
    postId = models.BigAutoField(primary_key=True)
    title = models.TextField(validators=[MaxLengthValidator(limit_value=64, message="Ограничение заголовка - 64 символа")], verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    photo = models.ImageField(upload_to="imgs/posts/", verbose_name="Картинка", blank=True, null=True)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    sendDate = models.DateTimeField(verbose_name="Дата отправки", null=True, default=django.utils.timezone.now)
    filter = models.ForeignKey("Filters", on_delete=models.CASCADE, verbose_name="Фильтр", blank=True, null=True)
    isSend = models.BooleanField(verbose_name="Отправлен ли", default=False)

    def clean(self):
        if self.photo and (len(self.text) + len(self.title) >= 1024):
            raise ValidationError("Пост с картинкой не должен быть длинее 1024 символов")
        elif not self.photo and (len(self.text) + len(self.title) > 4096):
            raise ValidationError("Пост не должен быть длинне 4096 символов")

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Books(models.Model):
    bookId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    startDate = models.DateField(verbose_name="Дата начала")
    endDate = models.DateField(verbose_name="Дата конца")
    goalSum = models.IntegerField(verbose_name="Необходимая сумма")
    collectedSum = models.IntegerField(default=0, verbose_name="Собранная сумма")
    link = models.CharField(max_length=256, verbose_name="Ссылка")
    isDone = models.BooleanField(default=False, verbose_name="Собрано ли")
    priceAfterDone = models.IntegerField(verbose_name="Цена после сбора")
    priceForSub = models.IntegerField(verbose_name="Цена для подписчика")
    priceCommon = models.IntegerField(verbose_name="Цена для всех")
    userId = models.ManyToManyField("Users", verbose_name="Заплатившие пользователи", blank=True)

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
    subscribesMenu = models.TextField(verbose_name="Меню покупки подписки ({subscribe})")
    activeSub = models.TextField(verbose_name="Формат подписки в меню ({end_date})")
    noSub = models.TextField(verbose_name="Отсутствие подписки")
    expiredSub = models.TextField(verbose_name="Подписка закончилась ({end_date})")
    buySubButton = models.CharField(max_length=64, verbose_name="Кнопка покупки подписки ({duration} - срок, {price} - цена)")
    alreadySubError = models.TextField(verbose_name="Ошибка уже имения подписки")
    usePromocodeButton = models.CharField(max_length=64, verbose_name="Кнопка использования промокода")
    promoInput = models.TextField(verbose_name="Инструкция по введению промокода")
    cancelPromoButton = models.CharField(max_length=64, verbose_name="Кнопка для отмены активного промокода")
    cancelPromoOk = models.TextField(verbose_name="Уведомлении об успешной отмене активного промокода")
    promoNotExists = models.TextField(verbose_name="Ошибка отсутствия промокода")
    promoAlreadyUsed = models.TextField(verbose_name="Промокод уже использован")
    promoOk = models.TextField(verbose_name="Уведомление об успешной активации промокода ({code}, {discount})")
    info = models.TextField(verbose_name="Информация")
    balanceMenu = models.TextField(verbose_name="Меню баланса ({balance}, {subscribe})")
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
    searchTextResult = models.TextField(verbose_name="Сообщение с результатом поиска в сообщении ({books})")
    searchFileResult = models.TextField(verbose_name="Сообщение с результатом поиска в файле")
    bookArchiveFormat = models.TextField(verbose_name="Формат вывода книги из архива ({id}, {author}, {title}, {year}, {genre}, {price})")
    bookInputError = models.TextField(verbose_name="Ошибка ввода номера книги")
    bookBuyMenu = models.TextField(verbose_name="Меню покупки книги ({book})")
    payButton = models.CharField(max_length=64, verbose_name="Кнопка оплаты")
    buyBookError = models.TextField(verbose_name="Ошибка при покупке книги")
    buyBookOk = models.TextField(verbose_name="Успешная покупка книги")
    payMenu = models.TextField(verbose_name="Сообщение при оплате")
    payError = models.TextField(verbose_name="Ошибка оплаты")
    payOk = models.TextField(verbose_name="Успешная оплата")
    checkPayButton = models.CharField(max_length=64, verbose_name="Кнопка для завершения оплаты")
    fundraisingMenu = models.TextField(verbose_name="Меню выбора книги фандрайзинг")
    payTitle = models.TextField(verbose_name="Заголовок")
    payDescription = models.TextField(verbose_name="Описание ({amount})")
    fundBookMenu = models.TextField(verbose_name="Меню с книгой фандрайзинга ({title}, {description}, {start}, {end}, {progress}, {price})")
    progressFormat = models.TextField(verbose_name="Формат прогресса ({percent})")
    yoomoneyMenu = models.TextField(verbose_name="Меню юмани")
    subDescription = models.TextField(verbose_name="Описание подписки")
    downloadButton = models.CharField(max_length=64, verbose_name="Кнопка скачать")
    showProgressButton = models.CharField(max_length=64, verbose_name="Кнопка отображения прогресса сбора")
    progressOn = models.TextField(verbose_name="Отображение прогресса включено")
    progressOff = models.TextField(verbose_name="Отображение прогресса выключено")
    telegramPayLimit = models.TextField(verbose_name="Минимальный лимит пополнения через Телеграм 60 рублей")
    bookDoneNotify = models.TextField(verbose_name="Уведомление пользователя о окончании сбора ({title})")
    closeButton = models.CharField(max_length=64, verbose_name="Кнопка закрыть")
    closeConfirm = models.TextField(verbose_name="Подтверждение закрытия")
    autoPayButtonOff = models.CharField(max_length=64, verbose_name="Кнопка выключения автоплатежа")
    autoPayButtonOn = models.CharField(max_length=64, verbose_name="Кнопка включения автоплатежа")
    autoPayOff = models.CharField(max_length=64, verbose_name="Выключение автоплатежа")
    autoPayOn = models.CharField(max_length=64, verbose_name="Включение автоплатежа")
    fundNotEndError = models.TextField(verbose_name="Сбор ещё не закончен")
    successAutoPay = models.CharField(max_length=64, verbose_name="Сообщение об успешном списании по подписке")
    subscribeOff = models.CharField(max_length=64, verbose_name="Сообщение об отключении подписки по неуплате")
    downloadResult = models.TextField(verbose_name="Вывод ссылки для скачивания ({link})")
    blockMenuInfo = models.CharField(max_length=128, verbose_name="Сообщение о блокировки выхода во время оплаты")

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
    code = models.CharField(max_length=128, verbose_name="Код", unique=True)
    link = models.CharField(max_length=256, verbose_name="Ссылка", blank=True, null=True)
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


class Statistic(models.Model):
    statisticsId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="Имя")
    allSubsCounter = models.IntegerField(default=0, verbose_name="Общее количество купивших подписку")
    noBuyUsersCounter = models.IntegerField(default=0, verbose_name="Количество пользователей не купивших подписку")
    blockUsersCounter = models.IntegerField(default=0, verbose_name="Количество пользователей заблокировавших бота")
    interruptedPaymentsCount = models.IntegerField(default=0, verbose_name="Количество прерванных оплат оплату")
    archiveBooksSum = models.IntegerField(default=0, verbose_name="Сумма покупок книг из архива")
    archiveBooksCount = models.IntegerField(default=0, verbose_name="Количество купленных книг из архива")

    def __repr__(self):
        return "Статистика"

    def __str__(self):
        return "Статистика"

    def get_absolute_url(self):
        return reverse("get_stats")

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"


class ArchiveStatistic(models.Model):
    archivebookId = models.IntegerField(primary_key=True)
    title = models.TextField(verbose_name="Заголовок")
    author = models.TextField(verbose_name="Автор")
    year = models.TextField(verbose_name="Год")
    genre = models.TextField(verbose_name="Жанр")
    link = models.TextField(verbose_name="Ссылка на книгу")
    price = models.TextField(verbose_name="Цена архивной книги")
    appeal = models.IntegerField(default=0, verbose_name="Кол-во обращений")
    buy_count = models.IntegerField(default=0, verbose_name="Кол-во покупок")

    def __repr__(self):
        return "Статистика архива книг"

    def __str__(self):
        return "Статистика архива книг"

    class Meta:
        verbose_name = "Статистика архива книг"
        verbose_name_plural = "Статистика архива книг"


class PaymentStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
