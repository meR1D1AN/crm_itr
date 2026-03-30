from django.db import models

from fixture.choices import EscChoices


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


class EscProblem(models.Model):
    esc = models.ForeignKey(
        Esc,
        on_delete=models.CASCADE,
        verbose_name="Эскалатор",
    )
    problem = models.CharField(
        max_length=255,
        verbose_name="Проблема",
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата проблемы",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Решено",
    )

    def __str__(self):
        return f"{self.esc} - {self.create_at}"

    class Meta:
        verbose_name = "Проблема"
        verbose_name_plural = "Проблемы"


class EscReplace(models.Model):
    esc = models.ForeignKey(
        Esc,
        on_delete=models.CASCADE,
        verbose_name="Эскалатор",
    )
    replace = models.CharField(
        max_length=255,
        verbose_name="Заменить",
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата замены",
    )
    resolved = models.BooleanField(
        default=False,
        verbose_name="Решено",
    )

    def __str__(self):
        return f"{self.esc} - {self.create_at}"

    class Meta:
        verbose_name = "Замена"
        verbose_name_plural = "Замены"


class EscTO(models.Model):
    esc = models.ForeignKey(
        Esc,
        on_delete=models.CASCADE,
        verbose_name="Эскалатор",
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата проведения ТО",
    )

    def __str__(self):
        return f"{self.esc} - {self.create_at}"

    class Meta:
        verbose_name = "ТО"
        verbose_name_plural = "ТО"
