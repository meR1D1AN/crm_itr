from django.db import models

from base.models import BuildingLiftEscBase


class TO(BuildingLiftEscBase):
    """
    Модель для записи проведения ТО, в каком здании, какой лифт или какой эскалатор, и когда проводилось.
    """

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата проведения технического обслуживания",
    )

    def __str__(self):
        if self.esc:
            return f"{self.building} - {self.esc} - {self.create_at}"
        return f"{self.building} - {self.elevator} - {self.create_at}"

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Техничение обслуживания"
