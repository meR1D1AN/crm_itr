from django.contrib import admin

from problems.models import Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "building",
        "elevator",
        "esc",
        "create_at",
        "problem",
        "resolved",
    )
    list_filter = ("building", "elevator", "esc", "resolved")
    list_display_links = list_display
    search_fields = ("problem",)
