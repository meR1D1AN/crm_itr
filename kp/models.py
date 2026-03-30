import datetime

from django.db import models

from base.choices import DeliveryTimeChoice, UnitChoice
from base.models import NULLABLE
from itr.models import Customer
from users.models import User


class KP(models.Model):
    # Номер КП
    number = models.CharField(max_length=20, verbose_name="Номер КП", help_text="Введите номер КП", **NULLABLE)
    # Дата создания КП
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания КП")
    # Заказчик
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="kps",
        verbose_name="Заказчик",
        help_text="Выберите заказчика",
        **NULLABLE,
    )
    # Цена действительна до
    price_valid_until = models.DateField(
        verbose_name="Цена действительна до",
        help_text="Введите дату, до которой цена действительна",
    )
    # Создана пользователем
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="kps",
        verbose_name="Создана пользователем",
        help_text="Выберите пользователя",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.number} - {self.customer.customer_name}"

    def save(self, *args, **kwargs):
        if not self.number:
            today = datetime.date.today()
            self.number = today.strftime("%d-%m-%y ") + str(KP.objects.count() + 1)
        KP, self.save(*args, **kwargs)

    class Meta:
        verbose_name = "КП"
        verbose_name_plural = "КП"
        ordering = ["-create_at"]


class KPDetail(models.Model):
    # КП
    kp = models.ForeignKey(KP, on_delete=models.CASCADE, related_name="items")
    # Наименование
    appellation = models.CharField(max_length=255, verbose_name="Наименование", help_text="Введите наименование КП")
    # Сроки поставки
    delivery_time = models.CharField(
        choices=DeliveryTimeChoice.choices,
        default=DeliveryTimeChoice.IN_STOCK,
        max_length=16,
        verbose_name="Сроки поставки",
        help_text="Выберите сроки поставки",
    )
    # Количество
    quantity = models.PositiveIntegerField(verbose_name="Количество", help_text="Введите количество")
    # Единица
    unit = models.CharField(
        choices=UnitChoice.choices,
        default=UnitChoice.UNIT_PC,
        max_length=5,
        verbose_name="Единица",
        help_text="Выберите единицу",
    )
    # Цена за единицу без НДС
    price_without_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу без НДС",
        help_text="Введите цену за единицу без НДС",
    )
    # Сумма без НДС
    sum_without_vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма без НДС",
        help_text="Введите сумму без НДС",
    )

    def save(self, *args, **kwargs):
        self.sum_without_vat = self.price_without_vat * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appellation} - {self.kp.number}"

    class Meta:
        verbose_name = "Позиция КП"
        verbose_name_plural = "Позиции КП"
        ordering = ["kp"]
