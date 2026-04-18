from datetime import date, datetime

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from .models import ActivityLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_activity(
    request,
    action,
    description,
    target_user=None,
    obj=None,
    changes=None,
):
    object_repr = None
    if obj:
        if hasattr(obj, "title") and obj.title:
            object_repr = str(obj.title)
        elif hasattr(obj, "name") and obj.name:
            object_repr = str(obj.name)
        elif hasattr(obj, "email") and obj.email:
            object_repr = str(obj.email)
        else:
            object_repr = str(obj)

    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        target_user=target_user,
        action=action,
        description=description,
        changes=changes or {},
        ip_address=get_client_ip(request),
        app_label=obj._meta.app_label if obj else None,
        model_name=obj.__class__.__name__ if obj else None,
        object_id=obj.pk if obj else None,
        object_repr=object_repr[:255] if object_repr else None,
        content_type=ContentType.objects.get_for_model(obj) if obj else None,
    )


def _coerce_initial_form_value(field, raw_value):
    if isinstance(field, forms.ModelMultipleChoiceField):
        if raw_value in (None, "", []):
            return []

        if hasattr(raw_value, "values_list"):
            pk_list = list(raw_value.values_list("pk", flat=True))
        elif isinstance(raw_value, (set, tuple, list)):
            pk_list = list(raw_value)
        else:
            pk_list = [raw_value]

        normalized_pks = [getattr(item, "pk", item) for item in pk_list]
        return list(field.queryset.filter(pk__in=normalized_pks))

    if isinstance(field, forms.ModelChoiceField):
        if raw_value in (None, "", []):
            return None

        if hasattr(raw_value, "pk"):
            raw_value = raw_value.pk
        elif hasattr(raw_value, "values_list"):
            pk_values = list(raw_value.values_list("pk", flat=True))
            raw_value = pk_values[0] if pk_values else None
        elif isinstance(raw_value, (set, tuple, list)):
            first_value = next(iter(raw_value), None)
            raw_value = getattr(first_value, "pk", first_value)

        if raw_value in (None, "", []):
            return None

        return field.queryset.filter(pk=raw_value).first()

    return raw_value


def _serialize_log_value(value):
    if value is None:
        return "-"

    if hasattr(value, "all") and callable(value.all):
        value = list(value.all())

    if isinstance(value, (list, tuple, set)):
        serialized = []
        for item in value:
            item_text = _serialize_log_value(item)
            if item_text and item_text != "-":
                serialized.append(item_text)

        if not serialized:
            return "-"
        return ", ".join(sorted(serialized))

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, Model):
        if hasattr(value, "name") and value.name:
            return str(value.name)
        if hasattr(value, "title") and value.title:
            return str(value.title)
        if hasattr(value, "email") and value.email:
            return str(value.email)
        return str(value)

    if hasattr(value, "name") and not isinstance(value, str):
        file_name = getattr(value, "name", "")
        if file_name:
            return str(file_name)

    text = str(value).strip()
    return text if text else "-"


def build_form_changes(form):
    changes = {}

    if not getattr(form, "changed_data", None):
        return changes

    for field_name in form.changed_data:
        field = form.fields.get(field_name)
        field_label = field.label if field and field.label else field_name.replace("_", " ").title()

        old_value = form.initial.get(field_name)
        if field:
            old_value = _coerce_initial_form_value(field, old_value)

        new_value = form.cleaned_data.get(field_name)

        old_serialized = _serialize_log_value(old_value)
        new_serialized = _serialize_log_value(new_value)

        if old_serialized == new_serialized:
            continue

        changes[field_name] = {
            "label": str(field_label),
            "old": old_serialized,
            "new": new_serialized,
        }

    return changes


def build_snapshot_changes(before, after, labels=None):
    labels = labels or {}
    changes = {}

    for key in sorted(set(before.keys()) | set(after.keys())):
        old_serialized = _serialize_log_value(before.get(key))
        new_serialized = _serialize_log_value(after.get(key))

        if old_serialized == new_serialized:
            continue

        changes[key] = {
            "label": labels.get(key, key.replace("_", " ").title()),
            "old": old_serialized,
            "new": new_serialized,
        }

    return changes



from collections import OrderedDict

from .models import Menu


def get_sidebar_menus_for_user(user):
    """
    Return:
    [
        {
            "menu": <Menu>,
            "children": [<Menu>, <Menu>]
        },
        ...
    ]
    """

    if not user.is_authenticated:
        return []

    # Superuser / admin -> all active menus
    if getattr(user, "is_superuser", False) or getattr(user, "is_admin", False):
        allowed_menus = (
            Menu.objects.filter(is_active=True)
            .select_related("parent")
            .prefetch_related("permissions")
            .order_by("order", "name")
        )
    else:
        role_ids = list(user.roles.values_list("id", flat=True)) if hasattr(user, "roles") else []

        allowed_menus = (
            Menu.objects.filter(
                is_active=True,
                role_menu_items__id__in=role_ids,
            )
            .select_related("parent")
            .prefetch_related("permissions")
            .distinct()
            .order_by("order", "name")
        )

        # direct permission-based visible menus
        permission_allowed_ids = []
        for menu in Menu.objects.filter(is_active=True).select_related("parent").prefetch_related("permissions"):
            if menu.user_can_access(user):
                permission_allowed_ids.append(menu.id)

        allowed_menus = (
            Menu.objects.filter(id__in=set(list(allowed_menus.values_list("id", flat=True)) + permission_allowed_ids))
            .select_related("parent")
            .prefetch_related("permissions")
            .distinct()
            .order_by("order", "name")
        )

    parents = []
    children_map = OrderedDict()

    for menu in allowed_menus:
        if menu.parent_id:
            children_map.setdefault(menu.parent_id, [])
            children_map[menu.parent_id].append(menu)
        else:
            parents.append(menu)

    sidebar_menus = []
    for parent in parents:
        sidebar_menus.append({
            "menu": parent,
            "children": children_map.get(parent.id, []),
        })

    # orphan child protect: parent না থাকলেও child user can access করলে parentless item হিসেবে দেখাও না
    return sidebar_menus