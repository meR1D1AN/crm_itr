"""
Кастомная группировка главной страницы и бокового меню админки.
"""

from __future__ import annotations

from django.contrib.admin.sites import AdminSite
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst

_original_get_app_list = AdminSite.get_app_list


def _model_dict(site: AdminSite, request, model) -> dict | None:
    model_admin = site._registry.get(model)
    if model_admin is None or not model_admin.has_module_permission(request):
        return None
    perms = model_admin.get_model_perms(request)
    if True not in perms.values():
        return None

    app_label = model._meta.app_label
    model_name = model._meta.model_name
    model_dict = {
        "model": model,
        "name": capfirst(model._meta.verbose_name_plural),
        "object_name": model._meta.object_name,
        "perms": perms,
        "admin_url": None,
        "add_url": None,
    }
    if perms.get("change") or perms.get("view"):
        model_dict["view_only"] = not perms.get("change")
        try:
            model_dict["admin_url"] = reverse(
                f"admin:{app_label}_{model_name}_changelist",
                current_app=site.name,
            )
        except NoReverseMatch:
            pass
    if perms.get("add"):
        try:
            model_dict["add_url"] = reverse(
                f"admin:{app_label}_{model_name}_add",
                current_app=site.name,
            )
        except NoReverseMatch:
            pass
    return model_dict


def _inject_user_into_auth_app_list(site: AdminSite, request, app_list: list) -> None:
    """Добавляет кастомного User (app users) в список моделей раздела auth."""
    if not app_list:
        return
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    if user_model._meta.app_label != "users":
        return
    row = _model_dict(site, request, user_model)
    if not row:
        return
    app = app_list[0]
    combined = [row] + [m for m in app["models"] if m["model"] != user_model]
    user_model_ref = user_model
    combined.sort(key=lambda m: (0 if m["model"] == user_model_ref else 1, m["name"].lower()))
    app["models"] = combined


def _section(site: AdminSite, request, title: str, app_label: str, models: list) -> dict | None:
    entries = []
    for m in models:
        row = _model_dict(site, request, m)
        if row:
            entries.append(row)
    if not entries:
        return None
    return {
        "name": title,
        "app_label": app_label,
        "app_url": "#",
        "has_module_perms": True,
        "models": entries,
    }


def _grouped_get_app_list(self: AdminSite, request, app_label=None):
    if app_label is not None:
        app_list = _original_get_app_list(self, request, app_label)
        if app_label == "auth":
            _inject_user_into_auth_app_list(self, request, app_list)
        return app_list

    from django.contrib.auth import get_user_model

    from buildings.models import Building
    from esc.models import Esc
    from lifts.models import Elevator
    from problems.models import Problem
    from replacements.models import Replacement
    from tos.models import TO

    grouped_models = {Building, Elevator, Esc, Problem, Replacement, TO}

    sections = [
        _section(self, request, "Здания", "group_buildings", [Building]),
        _section(
            self,
            request,
            "Лифты",
            "group_lifts",
            [Elevator, Problem, Replacement, TO],
        ),
        _section(
            self,
            request,
            "Эскалаторы",
            "group_escalators",
            [Esc, Problem, Replacement, TO],
        ),
    ]
    result = [s for s in sections if s is not None]

    rest = _original_get_app_list(self, request)
    filtered_rest = []
    users_models = []

    for app in rest:
        models = [m for m in app["models"] if m["model"] not in grouped_models]
        if not models:
            continue
        if app["app_label"] == "users":
            users_models = models
            continue
        filtered_rest.append({**app, "models": models})

    if users_models:
        user_model = get_user_model()
        merged = False
        for app in filtered_rest:
            if app["app_label"] == "auth":
                combined = list(users_models) + list(app["models"])
                combined.sort(
                    key=lambda m: (
                        0 if m["model"] == user_model else 1,
                        m["name"].lower(),
                    )
                )
                app["models"] = combined
                merged = True
                break
        if not merged:
            from django.apps import apps

            uc = apps.get_app_config("users")
            filtered_rest.insert(
                0,
                {
                    "name": uc.verbose_name,
                    "app_label": "users",
                    "app_url": "#",
                    "has_module_perms": True,
                    "models": users_models,
                },
            )

    result.extend(filtered_rest)

    return result


def install_grouped_admin_index() -> None:
    if getattr(AdminSite, "_grouped_index_installed", False):
        return
    AdminSite.get_app_list = _grouped_get_app_list
    AdminSite._grouped_index_installed = True
