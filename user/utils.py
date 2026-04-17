
from django.contrib.contenttypes.models import ContentType
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
):
    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        target_user=target_user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
        app_label=obj._meta.app_label if obj else None,
        model_name=obj.__class__.__name__ if obj else None,
        object_id=obj.pk if obj else None,
        object_repr=str(obj)[:255] if obj else None,
        content_type=ContentType.objects.get_for_model(obj) if obj else None,
    )



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