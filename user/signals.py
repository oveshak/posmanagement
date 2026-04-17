# from django.db.models.signals import post_save, post_delete
# from django.contrib.auth.signals import user_logged_in, user_logged_out
# from django.dispatch import receiver
# from django.contrib.contenttypes.models import ContentType

# from .models import ActivityLog, Users
# from .middleware import get_current_request, get_current_user


# EXCLUDED_MODELS = {"ActivityLog"}


# # def get_client_ip(request):
# #     if not request:
# #         return None

# #     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
# #     if x_forwarded_for:
# #         return x_forwarded_for.split(",")[0].strip()
# #     return request.META.get("REMOTE_ADDR")


# # def create_activity_entry(instance, action):
# #     model_name = instance.__class__.__name__

# #     if model_name in EXCLUDED_MODELS:
# #         return

# #     request = get_current_request()
# #     actor = get_current_user()

# #     if actor and not getattr(actor, "is_authenticated", False):
# #         actor = None

# #     target_user = instance if isinstance(instance, Users) else None

# #     ActivityLog.objects.create(
# #         user=actor,
# #         target_user=target_user,
# #         action=action,
# #         app_label=instance._meta.app_label,
# #         model_name=model_name,
# #         object_id=instance.pk,
# #         object_repr=str(instance),
# #         description=f"{action.title()} {model_name}: {instance}",
# #         ip_address=get_client_ip(request),
# #         content_type=ContentType.objects.get_for_model(instance.__class__),
# #     )


# @receiver(post_save)
# def auto_log_create_update(sender, instance, created, **kwargs):
#     if sender._meta.app_label != "user":
#         return
#     if sender.__name__ in EXCLUDED_MODELS:
#         return

#     action = "create" if created else "update"
#     create_activity_entry(instance, action)


# @receiver(post_delete)
# def auto_log_delete(sender, instance, **kwargs):
#     if sender._meta.app_label != "user":
#         return
#     if sender.__name__ in EXCLUDED_MODELS:
#         return

#     create_activity_entry(instance, "delete")


# @receiver(user_logged_in)
# def log_user_login(sender, request, user, **kwargs):
#     ActivityLog.objects.create(
#         user=user,
#         target_user=user,
#         action="login",
#         app_label=user._meta.app_label,
#         model_name=user.__class__.__name__,
#         object_id=user.pk,
#         object_repr=str(user),
#         description=f"Login: {user}",
#         ip_address=get_client_ip(request),
#         content_type=ContentType.objects.get_for_model(user.__class__),
#     )


# @receiver(user_logged_out)
# def log_user_logout(sender, request, user, **kwargs):
#     if not user:
#         return

#     ActivityLog.objects.create(
#         user=user,
#         target_user=user,
#         action="logout",
#         app_label=user._meta.app_label,
#         model_name=user.__class__.__name__,
#         object_id=user.pk,
#         object_repr=str(user),
#         description=f"Logout: {user}",
#         ip_address=get_client_ip(request),
#         content_type=ContentType.objects.get_for_model(user.__class__),
#     )



from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from .models import Users


def table_exists(table_name):
    return table_name in connection.introspection.table_names()


@receiver(post_save, sender=Users)
def sync_user_branch_area_staff(sender, instance, created, **kwargs):
    required_tables = {
        "user_branch_branch_staff",
        "user_area_area_staff",
        "user_customergroup_customer_group_staff",
    }

    existing_tables = set(connection.introspection.table_names())
    if not required_tables.issubset(existing_tables):
        return

    try:
        if instance.pk:
            instance.sync_staff_relations()
    except (OperationalError, ProgrammingError):
        return


@receiver(m2m_changed, sender=Users.customer_group.through)
def sync_user_customer_group_staff(sender, instance, action, **kwargs):
    required_tables = {
        "user_branch_branch_staff",
        "user_area_area_staff",
        "user_customergroup_customer_group_staff",
    }

    existing_tables = set(connection.introspection.table_names())
    if not required_tables.issubset(existing_tables):
        return

    try:
        if action in ["post_add", "post_remove", "post_clear"]:
            instance.sync_staff_relations()
    except (OperationalError, ProgrammingError):
        return