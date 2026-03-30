from django.db import models

from base.choices import EscChoices


class Esc(models.Model):
    esc = models.CharField(
        choices=EscChoices.choices,
        max_length=14,
        default=EscChoices.E11,
        verbose_name="Эскалатор",
        help_text="Выберите эскалатор",
    )

    def __str__(self):
        return self.get_esc_display()

    class Meta:
        verbose_name = "Эскалатор"
        verbose_name_plural = "Эскалаторы"
