from django.db import models

from base.models import BuildingLiftEscBase


class Problem(BuildingLiftEscBase):
    """
    Модель для записи проблем, в каком здании, какой лифт или какой эскалатор имеет проблему.
    """

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата проблемы",
    )
    problem = models.CharField(
        max_length=255,
        verbose_name="Проблема",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Решена?",
    )

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"

    def __str__(self):
        if self.esc:
            return f"{self.building} - {self.esc} - {self.create_at} [{self.resolved}]"
        return f"{self.building} - {self.elevator} - {self.create_at} [{self.resolved}]"
