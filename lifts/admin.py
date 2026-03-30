from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from lifts.models import Elevator


@admin.register(Elevator)
class ElevatorAdmin(admin.ModelAdmin):
    list_display = ("elevator", "buildings_list")

    def buildings_list(self, obj: Elevator) -> str:
        buildings = obj.buildings_lift.all()
        if not buildings:
            return "Нет зданий"
        return mark_safe("<br>".join(escape(str(b)) for b in buildings))

    buildings_list.short_description = "Здания"
