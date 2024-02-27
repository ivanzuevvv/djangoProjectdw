import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models import F


class Filial(models.Model):
    name_filial = models.CharField(max_length=50)


class Station(models.Model):
    name_ks = models.CharField(max_length=50)


class KcNumber(models.Model):
    number_ks = models.IntegerField()


class Event(models.Model):
    name = models.CharField(max_length=50)


class Mpn(models.Model):
    name = models.CharField(max_length=50)


class GpaNumber(models.Model):
    number = models.IntegerField()


class Plans(models.Model):
    number = models.CharField(max_length=50)


class Plan(models.Model):
    filial = models.ForeignKey(Filial, verbose_name='филиал', on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    kc = models.ForeignKey(KcNumber, on_delete=models.CASCADE)
    gpa = models.ForeignKey(GpaNumber, on_delete=models.CASCADE)
    mpn = models.ForeignKey(Mpn, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)


class Kc(models.Model):
    number = models.ForeignKey(KcNumber, on_delete=models.CASCADE)


class GpaModification(models.Model):
    name = models.CharField(max_length=50)


class Complete(models.Model):
    number = models.IntegerField()


class IsNotNecessary(models.Model):
    number = models.IntegerField()


class Marks(models.Model):
    number = models.IntegerField()


class Notes(models.Model):
    text = models.CharField(max_length=60)


class SauModification(models.Model):
    name = models.CharField(max_length=50)


class Position(models.Model):
    name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    level = models.IntegerField()


class Execution(models.Model):
    filial = models.ForeignKey(Filial, verbose_name='Филиал', on_delete=models.CASCADE)
    station = models.ForeignKey(Station, verbose_name='Станция', on_delete=models.CASCADE)
    kc = models.ForeignKey(KcNumber, verbose_name='Кс', on_delete=models.CASCADE)
    gpa_number = models.IntegerField(verbose_name="Номер Гпа", null=True)
    gpa_modification = models.ForeignKey(GpaModification, verbose_name='Модификация ГПА', on_delete=models.CASCADE)
    sau_modification = models.ForeignKey(SauModification, verbose_name='Модификация САУ', on_delete=models.CASCADE)
    mpn = models.ForeignKey(Mpn, verbose_name='МПН', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    defects_count = models.IntegerField(verbose_name='Наработка')
    months = models.CharField(max_length=50, verbose_name='месяца')
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    event = models.ForeignKey(Event, verbose_name='Мероприятия', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, verbose_name='Позиция', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Наработка СА'
        verbose_name_plural = 'Наработка СА'


class Cvartals(models.Model):
    Q1 = '1 квартал'
    Q2 = '2 квартал'
    Q3 = '3 квартал'
    Q4 = '4 квартал'

    QUARTER_CHOICES = [
        (Q1, '1 квартал'),
        (Q2, '2 квартал'),
        (Q3, '3 квартал'),
        (Q4, '4 квартал'),
    ]

    name = models.CharField(max_length=100, db_index=True, verbose_name="Квартал", blank=True, null=True,
                            choices=QUARTER_CHOICES)

    def __str__(self):
        return self.name

    @classmethod
    def get_current_quarter(cls):
        month = datetime.datetime.now().month
        if month in [1, 2, 3]:
            return cls.Q1
        elif month in [4, 5, 6]:
            return cls.Q2
        elif month in [7, 8, 9]:
            return cls.Q3
        else:
            return cls.Q4

    def __str__(self):
        return self.name


class Even(models.Model):
    station = models.CharField(max_length=50, null=True, verbose_name="Cтанция")
    department = models.CharField(max_length=500, null=True, verbose_name="Цех")
    gpa_number = models.IntegerField(verbose_name="Номер Гпа", max_length=50, null=True)
    sau_modifications = models.CharField(max_length=100, null=True, verbose_name="Модификация САУ")
    complete = models.IntegerField(max_length=50, verbose_name="Выполнено", blank=True, null=True, default=0,)
    plan = models.IntegerField(verbose_name="План", null=True)
    isnotnecessary = models.CharField(max_length=15, blank=True, null=True, verbose_name='Не требуется', choices=[('Да', 'Да'), ('Нет', 'Нет')])
    done = models.IntegerField(max_length=50, verbose_name="Выполнено", default=0, blank=True, null=True, )
    text = models.CharField(max_length=50, verbose_name="Примечания", blank=True, null=True)
    cvartal1 = models.PositiveIntegerField(verbose_name="Квартал 1", blank=True, null=True, default=0)
    cvartal2 = models.PositiveIntegerField(verbose_name="Квартал 2", blank=True, null=True, default=0)
    cvartal3 = models.PositiveIntegerField(verbose_name="Квартал 3", blank=True, null=True, default=0)
    cvartal4 = models.PositiveIntegerField(verbose_name="Квартал 4", blank=True, null=True, default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def total_complete(self):
        return Even.objects.filter(category=self.category).aggregate(Sum('complete'))['complete__sum']
    total_complete.short_description = 'Сумма выполненных работ'

    def str(self):
        return self.station

    class Meta:
        verbose_name = 'Мероприятия'
        verbose_name_plural = 'Мероприятия'

    def is_complete(self):
        return self.complete >= self.plan

    @classmethod
    def completed(cls):
        return cls.objects.filter(complete__gte=F('plan'))

    @classmethod
    def not_completed(cls):
        return cls.objects.filter(complete__lt=F('plan'))


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория", blank=True, null=True)
    summa = models.IntegerField(verbose_name="cумма", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Narabotka(models.Model):
    refuses = models.IntegerField(max_length=500)
    refuses_kip = models.IntegerField(max_length=500)

    class Meta:
        verbose_name = 'Отказы не приведших к АО'
        verbose_name_plural = 'Отказы не приведших к АО'


class Otkaz(models.Model):
    lpu = models.CharField(max_length=500, verbose_name="Лпу")
    net = models.IntegerField(max_length=500)
    date = models.DateField(verbose_name='Дата')
    vidotkaza = models.CharField(max_length=500, verbose_name="Лпу")

    class Meta:
        verbose_name = 'Приведшие к АО отказы СА'
        verbose_name_plural = 'Приведшие к АО отказы СА'


class Vnerdenie(models.Model):
    lpu = models.CharField(max_length=500, verbose_name="Лпу")
    department = models.CharField(max_length=500, verbose_name="Цех")
    gpa_number = models.IntegerField(verbose_name="Номер Гпа", max_length=50, null=True)
    ip = models.CharField(max_length=500, verbose_name="Наименование ИП")
    type_equipment = models.CharField(max_length=500, verbose_name="Тип оборудования")
    ip_number = models.CharField(verbose_name="Номер Ип", max_length=50, null=True, )
    done = models.CharField(max_length=50, verbose_name="Выполнено", blank=True, null=True, choices=[('Да', 'Да'), ('Нет', 'Нет')])
    reason = models.CharField(max_length=50, verbose_name="Причина не выполнения", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Информ письма'
        verbose_name_plural = 'Информ письма'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT, verbose_name="пользователь")
    status = models.CharField(default='Обычный', verbose_name='статус пользователя', max_length=20)
    city = models.CharField(max_length=50, blank=True, null=True)

    def get_upload_url(self):
        return self.avatar.url


class Category1(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория", blank=True, null=True)
    summa = models.IntegerField(verbose_name="cумма", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория для графика'
        verbose_name_plural = 'Категория для графика'


class Document3(models.Model):
    ip = models.CharField(max_length=500, verbose_name="Ип")
    ip_code = models.CharField(max_length=500, verbose_name="Ип код")
    naim_ip = models.CharField(max_length=500, verbose_name="Наименование Ип")
    type_gpa = models.CharField(max_length=500, verbose_name="Тип Гпа")
    type_equiomentt = models.CharField(max_length=500, verbose_name="Вид оборудование")
    type_equioment = models.CharField(max_length=500, verbose_name="Тип оборудование")
    filial = models.CharField(max_length=500, verbose_name="Тип филиал")
    date = models.DateField(verbose_name='Дата')
    document3 = models.FileField(upload_to='documents3/')
    text = models.CharField(max_length=50, verbose_name="Примечания", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Реестр ИП'
        verbose_name_plural = 'Реестр ИП'


class Category5(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Выполнено", blank=True, null=True)

    def __str__(self):
        return self.name


class Control(models.Model):
    lpu = models.CharField(max_length=500, verbose_name="Лпу")
    station = models.CharField(max_length=50, null=True, verbose_name="Кс")
    department = models.CharField(max_length=500, verbose_name="Цех")
    gpa_number = models.IntegerField(verbose_name="Номер Гпа", max_length=50, null=True)
    gpa_typle = models.CharField(max_length=100, null=True, verbose_name="Тип Гпа")
    sau_modifications = models.CharField(max_length=100, null=True, verbose_name="Модификация САУ")
    type_equioment = models.CharField(max_length=500, verbose_name="Тип оборудование")
    ip = models.CharField(max_length=500, verbose_name="Ип")
    n_ip = models.CharField(max_length=500, verbose_name="Наименование Ип")
    data_complete = models.CharField(max_length=200, verbose_name='дата выполнения')
    complete = models.CharField(max_length=50, verbose_name="Выполнено", blank=True, null=True,choices=[('Да', 'Да')])
    category5 = models.ForeignKey('Category5', on_delete=models.PROTECT, verbose_name="выполнено", blank=True, null=True)
    text = models.CharField(max_length=50, verbose_name="Примечания", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Контроль внедрения'
        verbose_name_plural = 'Контроль внедрения'


class Document5(models.Model):
    name = models.CharField(max_length=500, verbose_name="Имя")
    document = models.FileField(upload_to='documents5/')

    class Meta:
        verbose_name = 'Документация'
        verbose_name_plural = 'Документация'


class Document1(models.Model):
    name = models.CharField(max_length=500, verbose_name="Имя")
    document1 = models.FileField(upload_to='documents1/')

    class Meta:
        verbose_name = 'Рац предложения'
        verbose_name_plural = 'Рац предложения'


class Predicions(models.Model):
    type_refuses = models.CharField(max_length=500, verbose_name="тип отказа")
    type_gpa = models.CharField(max_length=500, verbose_name="Тип ГПА")
    type_say = models.CharField(max_length=500, verbose_name="Тип САУ")
    type_equioment = models.CharField(max_length=500, verbose_name="Внешнее проявления отказа")
    element = models.CharField(max_length=500, verbose_name="Подробное описание причины отказа")
    refuses_element = models.CharField(max_length=500, verbose_name="Элемента отказа")
    maybe_reasons = models.CharField(max_length=500, verbose_name="Отказавший элемент")
    meropriation = models.CharField(max_length=500, verbose_name="Содержание Мероприятия")

    class Meta:
        verbose_name = 'Экспертная система отказ СА'
        verbose_name_plural = 'Экспертная система отказ СА'


