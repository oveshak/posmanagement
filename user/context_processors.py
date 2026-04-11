# from django.db.models import Q
# from .models import Menu


# def user_menus_context(request):
#     """Context processor to provide user's accessible menus"""
#     context = {
#         'user_menus': [],
#         'main_menus': [],
#         'submenu_map': {},
#     }

#     if not request.user.is_authenticated:
#         return context

#     # Admin users see all menus
#     if request.user.is_admin or request.user.is_staff:
#         all_menus = Menu.objects.filter(is_active=True, parent=None).prefetch_related('submenus').order_by('order')
#         context['main_menus'] = all_menus
        
#         # Create submenu map
#         for menu in all_menus:
#             context['submenu_map'][menu.id] = menu.get_submenus()
#     else:
#         # Regular users see menus based on their roles
#         from .models import Roles
        
#         user_roles = request.user.roles.all()
#         role_menu_ids = set()
        
#         for role in user_roles:
#             role_menu_ids.update(role.menu.values_list('id', flat=True))
        
#         # Get only main menus (parent=None)
#         main_menus = Menu.objects.filter(
#             id__in=role_menu_ids,
#             is_active=True,
#             parent=None
#         ).prefetch_related('submenus').order_by('order')
        
#         context['main_menus'] = main_menus
        
#         # Create submenu map for accessible submenus
#         for menu in main_menus:
#             submenus = menu.submenus.filter(is_active=True, id__in=role_menu_ids).order_by('order')
#             if submenus.exists():
#                 context['submenu_map'][menu.id] = submenus
    
#     context['user_menus'] = context['main_menus']
#     return context


# from django.db.models import Prefetch

# from .models import Menu


# def sidebar_menus(request):
#     user = getattr(request, "user", None)
#     if not user or not user.is_authenticated:
#         return {"sidebar_menus": []}

#     if getattr(user, "is_superuser", False) or getattr(user, "is_admin", False):
#         allowed_ids = list(Menu.objects.filter(is_active=True).values_list("id", flat=True))
#     else:
#         allowed_ids = list(
#             Menu.objects.filter(is_active=True, role_menu_items__user_roles=user)
#             .distinct()
#             .values_list("id", flat=True)
#         )

#     all_menus = Menu.objects.filter(id__in=allowed_ids, is_active=True).prefetch_related("permissions", "submenus__permissions").order_by("order", "name")

#     roots = []
#     for menu in all_menus.filter(parent__isnull=True):
#         children = [child for child in menu.submenus.all() if child.id in allowed_ids and child.user_can_access(user)]
#         if menu.user_can_access(user) or children:
#             roots.append({"menu": menu, "children": children})

#     return {"sidebar_menus": roots}






from .models import Menu


def sidebar_menus(request):
    user = getattr(request, "user", None)

    if not user or not user.is_authenticated:
        return {"sidebar_menus": []}

    if getattr(user, "is_superuser", False) or getattr(user, "is_admin", False):
        allowed_ids = list(
            Menu.objects.filter(is_active=True).values_list("id", flat=True)
        )
    else:
        allowed_ids = list(
            Menu.objects.filter(
                is_active=True,
                role_menu_items__user_roles=user
            ).distinct().values_list("id", flat=True)
        )

    menus = Menu.objects.filter(
        id__in=allowed_ids,
        is_active=True
    ).prefetch_related("submenus").order_by("order", "name")

    roots = []
    for menu in menus.filter(parent__isnull=True):
        children = [child for child in menu.submenus.all() if child.id in allowed_ids]
        roots.append({
            "menu": menu,
            "children": children
        })

    return {"sidebar_menus": roots}


def user_menus_context(request):
    return sidebar_menus(request)