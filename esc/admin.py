from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from esc.models import Esc


@admin.register(Esc)
class EscAdmin(admin.ModelAdmin):
    list_display = ("esc", "buildings_list")

    def buildings_list(self, obj: Esc) -> str:
        buildings = obj.buildings_esc.all()
        if not buildings:
            return "Нет зданий"
        return mark_safe("<br>".join(escape(str(b)) for b in buildings))

    buildings_list.short_description = "Здания"
