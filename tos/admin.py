from django.contrib import admin

from tos.models import TO


@admin.register(TO)
class TOAdmin(admin.ModelAdmin):
    list_display = (
        "building",
        "elevator",
        "esc",
        "create_at",
    )
    list_display_links = list_display
    list_filter = ("building", "elevator", "esc", "create_at")
