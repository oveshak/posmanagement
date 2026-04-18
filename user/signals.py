
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