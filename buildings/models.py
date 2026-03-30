from django.db import models

from base.choices import AddressChoices
from esc.models import Esc
from lifts.models import Elevator


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
        related_name="buildings_lift",
    )
    escs = models.ManyToManyField(
        Esc,
        verbose_name="Эскалаторы",
        related_name="buildings_esc",
    )

    def __str__(self):
        return self.get_address_display()

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"
