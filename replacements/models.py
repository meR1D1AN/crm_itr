from django.db import models

from base.models import BuildingLiftEscBase


class Replacement(BuildingLiftEscBase):
    """
    Модель для записи, в каком здании, какой лифт или какой эскалатор требует, чтобы в нём что-то заменили.
    """

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата замены",
    )
    info_replacement = models.TextField(
        verbose_name="Что стоит заменить",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Заменено?",
    )

    def __str__(self):
        if self.esc:
            return f"{self.building} - {self.esc} - {self.create_at} [{self.resolved}]"
        return f"{self.building} - {self.elevator} - {self.create_at} [{self.resolved}]"

    class Meta:
        verbose_name = "Замена"
        verbose_name_plural = "Замены"
