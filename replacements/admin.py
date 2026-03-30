from django.contrib import admin

from replacements.models import Replacement


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = (
        "building",
        "elevator",
        "esc",
        "create_at",
        "info_replacement",
        "resolved",
    )
    list_filter = ("building", "elevator", "esc", "resolved")
    list_display_links = list_display
    search_fields = ("info_replacement",)
