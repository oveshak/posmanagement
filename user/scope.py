

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

    has_branch = bool(user.branch_id)
    has_area = bool(user.area_id)
    has_customer_group = bool(user_customer_group_ids)
    has_multi_branch = bool(multi_branch_ids)

    has_any_assignment = has_branch or has_area or has_customer_group or has_multi_branch

    # If nothing selected on user profile => show all, then UI selected chain will work
    if not has_any_assignment:
        return {
            "branches": branches.distinct(),
            "areas": areas.distinct(),
            "customer_groups": customer_groups.distinct(),
        }

    allowed_branch_ids = set()
    allowed_area_ids = set()
    allowed_customer_group_ids = set()

    # 1) branch selected -> only that branch
    if user.branch_id:
        allowed_branch_ids.add(user.branch_id)

    # 2) area selected -> area + its parent branch
    if user.area_id:
        allowed_area_ids.add(user.area_id)
        if user.area and user.area.parent_branch_id:
            allowed_branch_ids.add(user.area.parent_branch_id)

    # 3) customer group selected -> cg + derive area + branch
    if user_customer_group_ids:
        allowed_customer_group_ids.update(user_customer_group_ids)

        cg_qs = CustomerGroup.objects.filter(id__in=user_customer_group_ids)

        allowed_branch_ids.update(
            cg_qs.exclude(branch_id__isnull=True).values_list("branch_id", flat=True)
        )
        allowed_area_ids.update(
            cg_qs.exclude(area_id__isnull=True).values_list("area_id", flat=True)
        )

    # 4) multi branch selected -> all those branches allowed
    if multi_branch_ids:
        allowed_branch_ids.update(multi_branch_ids)

    # ---------------------------------------
    # Build final base scope
    # ---------------------------------------

    # Branch rules:
    # - if branch selected => only that branch
    # - else if derived/allowed branch ids => those branches
    if allowed_branch_ids:
        branches = branches.filter(id__in=allowed_branch_ids)
    else:
        branches = Branch.objects.none()

    # Area rules:
    # - if branch + area selected => only that area
    # - elif area selected => only that area
    # - elif branch selected/multibranch => all areas under allowed branches
    if user.branch_id and user.area_id:
        areas = areas.filter(id=user.area_id, parent_branch_id=user.branch_id)

    elif user.area_id:
        areas = areas.filter(id=user.area_id)

    elif allowed_branch_ids:
        areas = areas.filter(parent_branch_id__in=allowed_branch_ids)

    else:
        areas = Area.objects.none()

    # Customer group rules:
    # - if branch + area + customer group selected => only those customer groups
    # - elif branch + area selected => all CG under that branch+area
    # - elif branch selected => all CG under that branch
    # - elif only customer group selected => only those
    # - elif multibranch selected => all CG under allowed branches
    if user.branch_id and user.area_id and user_customer_group_ids:
        customer_groups = customer_groups.filter(
            id__in=user_customer_group_ids,
            branch_id=user.branch_id,
            area_id=user.area_id,
        )

    elif user.branch_id and user.area_id:
        customer_groups = customer_groups.filter(
            branch_id=user.branch_id,
            area_id=user.area_id,
        )

    elif user.branch_id and user_customer_group_ids:
        customer_groups = customer_groups.filter(
            id__in=user_customer_group_ids,
            branch_id=user.branch_id,
        )

    elif user.branch_id:
        customer_groups = customer_groups.filter(branch_id=user.branch_id)

    elif user_customer_group_ids:
        customer_groups = customer_groups.filter(id__in=user_customer_group_ids)

    elif allowed_branch_ids:
        customer_groups = customer_groups.filter(branch_id__in=allowed_branch_ids)

    else:
        customer_groups = CustomerGroup.objects.none()

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
        customer_groups = customer_groups.filter(area_id=selected_area)

    if selected_customer_group_ids:
        customer_groups = customer_groups.filter(id__in=selected_customer_group_ids)

    return {
        "branches": branches.distinct(),
        "areas": areas.distinct(),
        "customer_groups": customer_groups.distinct(),
    }