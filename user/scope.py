

from .models import Branch, Area, CustomerGroup


def is_global_user(user):
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or getattr(user, "is_admin", False))
    )


def get_multibranch_branch_ids(user):
    if not user or not user.is_authenticated:
        return []

    return list(
        Branch.objects.filter(
            multibranch_sets__in=user.mult_branch.all()
        ).values_list("id", flat=True).distinct()
    )


def get_user_scope(user):
    """
    Base accessible scope.
    This decides what the user is allowed to see before UI-selected filters apply.
    """

    branches = Branch.objects.all().order_by("name")
    areas = Area.objects.select_related("parent_branch").all().order_by("name")
    customer_groups = CustomerGroup.objects.select_related("branch", "area").all().order_by("name")

    if not user or not user.is_authenticated:
        return {
            "branches": Branch.objects.none(),
            "areas": Area.objects.none(),
            "customer_groups": CustomerGroup.objects.none(),
        }

    if is_global_user(user):
        return {
            "branches": branches.distinct(),
            "areas": areas.distinct(),
            "customer_groups": customer_groups.distinct(),
        }

    user_customer_group_ids = set(user.customer_group.values_list("id", flat=True))
    multi_branch_ids = set(get_multibranch_branch_ids(user))

    has_any_assignment = bool(user.branch_id or user.area_id or user_customer_group_ids or multi_branch_ids)

    # If nothing selected on user profile => show all, then UI selected chain will work
    if not has_any_assignment:
        return {
            "branches": branches.distinct(),
            "areas": areas.distinct(),
            "customer_groups": customer_groups.distinct(),
        }

    # Priority chain (strict): branch => area => customer group => multibranch

    if user.branch_id:
        branches = branches.filter(id=user.branch_id)

        if user.area_id:
            areas = areas.filter(id=user.area_id, parent_branch_id=user.branch_id)
        else:
            areas = areas.filter(parent_branch_id=user.branch_id)

        if user.area_id and user_customer_group_ids:
            customer_groups = customer_groups.filter(
                id__in=user_customer_group_ids,
                branch_id=user.branch_id,
                area_id=user.area_id,
            )
        elif user.area_id:
            customer_groups = customer_groups.filter(
                branch_id=user.branch_id,
                area_id=user.area_id,
            )
        elif user_customer_group_ids:
            customer_groups = customer_groups.filter(
                id__in=user_customer_group_ids,
                branch_id=user.branch_id,
            )
        else:
            customer_groups = customer_groups.filter(branch_id=user.branch_id)

        return {
            "branches": branches.distinct().order_by("name"),
            "areas": areas.distinct().order_by("name"),
            "customer_groups": customer_groups.distinct().order_by("name"),
        }

    if user.area_id:
        areas = areas.filter(id=user.area_id)
        branch_ids = set(areas.values_list("parent_branch_id", flat=True))
        branches = branches.filter(id__in=branch_ids)

        if user_customer_group_ids:
            customer_groups = customer_groups.filter(
                id__in=user_customer_group_ids,
                area_id=user.area_id,
            )
        else:
            customer_groups = customer_groups.filter(area_id=user.area_id)

        return {
            "branches": branches.distinct().order_by("name"),
            "areas": areas.distinct().order_by("name"),
            "customer_groups": customer_groups.distinct().order_by("name"),
        }

    if user_customer_group_ids:
        customer_groups = customer_groups.filter(id__in=user_customer_group_ids)
        branch_ids = set(customer_groups.exclude(branch_id__isnull=True).values_list("branch_id", flat=True))
        area_ids = set(customer_groups.exclude(area_id__isnull=True).values_list("area_id", flat=True))

        branches = branches.filter(id__in=branch_ids)
        areas = areas.filter(id__in=area_ids)

        return {
            "branches": branches.distinct().order_by("name"),
            "areas": areas.distinct().order_by("name"),
            "customer_groups": customer_groups.distinct().order_by("name"),
        }

    # Fallback only when branch/area/customer group are not selected: multibranch scope
    branches = branches.filter(id__in=multi_branch_ids)
    areas = areas.filter(parent_branch_id__in=multi_branch_ids)
    customer_groups = customer_groups.filter(branch_id__in=multi_branch_ids)

    return {
        "branches": branches.distinct().order_by("name"),
        "areas": areas.distinct().order_by("name"),
        "customer_groups": customer_groups.distinct().order_by("name"),
    }


def apply_selected_filters(
    branches,
    areas,
    customer_groups,
    selected_branch="",
    selected_area="",
    selected_customer_group_ids=None,
):
    """
    UI selected dropdown filters.
    Works for:
    - no assignment user
    - multi branch user
    - branch assigned user
    - branch + area assigned user
    - branch + area + customer group assigned user
    """
    selected_customer_group_ids = [str(i) for i in (selected_customer_group_ids or []) if i]

    if selected_branch:
        branches = branches.filter(id=selected_branch)
        areas = areas.filter(parent_branch_id=selected_branch)
        customer_groups = customer_groups.filter(branch_id=selected_branch)

    if selected_area:
        areas = areas.filter(id=selected_area)
        # Keep branch in sync with selected area when area chosen directly.
        branches = branches.filter(id__in=areas.values_list("parent_branch_id", flat=True))
        customer_groups = customer_groups.filter(area_id=selected_area)

    if selected_customer_group_ids:
        customer_groups = customer_groups.filter(id__in=selected_customer_group_ids)
        # Keep branch/area synced with selected customer group(s), but do not
        # override an explicitly selected branch/area from the UI (edit forms).
        if not selected_branch:
            branches = branches.filter(id__in=customer_groups.values_list("branch_id", flat=True))
        if not selected_area:
            areas = areas.filter(id__in=customer_groups.values_list("area_id", flat=True))

    return {
        "branches": branches.distinct(),
        "areas": areas.distinct(),
        "customer_groups": customer_groups.distinct(),
    }