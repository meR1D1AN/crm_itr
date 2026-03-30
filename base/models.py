from django.db import models

NULLABLE = {"null": True, "blank": True}


class BuildingLiftEscBase(models.Model):
    """
    Общие связи: здание и ровно один из объектов — лифт или эскалатор (через XOR в дочерних моделях).
    related_name с %(class)s даёт уникальные обратные имена у Building / Elevator / Esc.
    """

    building = models.ForeignKey(
        "buildings.Building",
        on_delete=models.CASCADE,
        verbose_name="Здание",
        related_name="%(class)s_building",
    )
    elevator = models.ForeignKey(
        "lifts.Elevator",
        on_delete=models.CASCADE,
        verbose_name="Лифт",
        related_name="%(class)s_elevator",
        **NULLABLE,
    )
    esc = models.ForeignKey(
        "esc.Esc",
        on_delete=models.CASCADE,
        verbose_name="Эскалатор",
        related_name="%(class)s_esc",
        **NULLABLE,
    )

    class Meta:
        abstract = True
