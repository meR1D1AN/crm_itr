from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from buildings.models import Building


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "elevators_list",
        "escs_list",
    )

    def elevators_list(self, obj: Building) -> str:
        elevators = obj.elevators.all()
        if not elevators:
            return "Нет лифтов"
        return mark_safe("<br>".join(escape(str(e)) for e in elevators))

    def escs_list(self, obj: Building) -> str:
        escs = obj.escs.all()
        if not escs:
            return "Нет эскалаторов"
        return mark_safe("<br>".join(escape(str(e)) for e in escs))

    elevators_list.short_description = "Лифты"
    escs_list.short_description = "Эскалаторы"
