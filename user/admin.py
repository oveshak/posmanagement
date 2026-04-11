from django.contrib import admin
from .models import Menu, Roles, Branch, Area, CustomerGroup, MultiBranch, Users, ActivityLog


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "url", "order", "is_active")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "url")
    filter_horizontal = ("permissions",)


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("menu", "permissions")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "manager")
    search_fields = ("name", "phone")
    filter_horizontal = ("branch_staff",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_branch")
    search_fields = ("name",)
    list_filter = ("parent_branch",)
    filter_horizontal = ("area_staff",)


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "area", "customer_leader")
    search_fields = ("name", "customer_leader")
    list_filter = ("branch", "area")
    filter_horizontal = ("customer_group_staff",)


@admin.register(MultiBranch)
class MultiBranchAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    filter_horizontal = ("multi_branch",)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "branch", "area", "is_admin", "is_staff", "status")
    search_fields = ("email", "name", "username", "phone_number")
    list_filter = ("is_admin", "is_staff", "status", "branch", "area")
    filter_horizontal = ("roles", "customer_group", "mult_branch")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "model_name", "object_repr", "created_at")
    search_fields = ("description", "model_name", "object_repr")
    list_filter = ("action", "created_at")