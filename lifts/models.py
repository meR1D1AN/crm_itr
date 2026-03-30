from django.db import models

from fixture.choices import AddressChoices, ElevatorChoices


class Elevator(models.Model):
    """
    Класс для лифтов
    """

    elevator = models.CharField(
        choices=ElevatorChoices.choices,
        max_length=20,
        verbose_name="Лифт",
        help_text="Выбери лифт",
    )

    def __str__(self):
        return f"{self.get_elevator_display()}"

    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "Лифты"


class Building(models.Model):
    """
    Класс для записи адресов зданий с лифтами
    """

    address = models.CharField(
        choices=AddressChoices.choices,
        max_length=14,
        default=AddressChoices.D36,
        verbose_name="Адрес",
        help_text="Выбери адрес",
    )
    elevators = models.ManyToManyField(
        Elevator,
        verbose_name="Лифты",
        related_name="buildings",
        blank=True,
    )

    def __str__(self):
        return self.get_address_display()

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"


class Problem(models.Model):
    """
    Класс для записи проблем, и если проблема решена, то она помечена как решена
    """

    buildings = models.ForeignKey(
        Building,
        verbose_name="Здание",
        related_name="problems",
        on_delete=models.SET_NULL,
        null=True,
    )
    elevator = models.ForeignKey(
        Elevator,
        on_delete=models.CASCADE,
        verbose_name="Лифт",
        related_name="problems",
    )
    problem = models.TextField(
        verbose_name="Информация о проблеме",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Решено",
    )

    def __str__(self):
        return f"{self.problem} ({self.resolved})"

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"


class Replacement(models.Model):
    """
    Класс для записи, что стоит заменить
    """

    buildings = models.ForeignKey(
        Building,
        verbose_name="Здание",
        related_name="replacements",
        on_delete=models.CASCADE,
    )
    elevator = models.ForeignKey(
        Elevator,
        on_delete=models.CASCADE,
        verbose_name="Лифт",
    )
    info_problem = models.TextField(
        verbose_name="Что стоит заменить",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Решено",
    )

    def __str__(self):
        return self.info_problem

    class Meta:
        verbose_name = "Ремонт"
        verbose_name_plural = "Ремонты"


class TO(models.Model):
    """
    Класс проведения ТО на лифтах, какой лифт, и когда проводился
    """

    building = models.ForeignKey(
        Building,
        on_delete=models.SET_NULL,
        verbose_name="Здание",
        related_name="to",
        null=True,
    )
    elevator = models.ForeignKey(
        Elevator,
        on_delete=models.CASCADE,
        verbose_name="Лифт",
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата проведения ТО",
    )

    def __str__(self):
        return f"{self.elevator} - {self.date}"

    class Meta:
        verbose_name = "ТО"
        verbose_name_plural = "ТО"
