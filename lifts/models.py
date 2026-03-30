from django.db import models

from base.choices import ElevatorChoices


class Elevator(models.Model):
    """
    Модель для лифтов.
    """

    elevator = models.CharField(
        choices=ElevatorChoices.choices,
        max_length=20,
        verbose_name="Лифт",
        help_text="Выберите лифт",
    )

    def __str__(self):
        return self.get_elevator_display()

    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "Лифты"
