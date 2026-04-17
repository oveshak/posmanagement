
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Permission,
)
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords
from globalapp.models import Common
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# -------------------------
# MENU / ROLE
# -------------------------
from django.contrib.auth.models import Permission
from django.db import models
from django.urls import reverse, NoReverseMatch
from simple_history.models import HistoricalRecords

from globalapp.models import Common


class Menu(Common):
    name = models.CharField(max_length=100, verbose_name="Menu Name")
    icon = models.CharField(
        max_length=50,
        default="fas fa-circle",
        verbose_name="Font Awesome Icon",
        help_text="e.g. fas fa-users",
    )
    url = models.CharField(
        max_length=255,
        verbose_name="URL or URL Name",
        help_text="Example: user:user_list or /user/users/",
    )
    order = models.IntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="submenus",
        verbose_name="Parent Menu",
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="sidebar_menus",
        verbose_name="Required permissions",
        help_text="Leave empty if every authenticated user with this menu can open it.",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = ["order", "name"]
        unique_together = [["name", "parent"]]
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return f"{self.parent.name} → {self.name}" if self.parent else self.name

    def get_absolute_url_or_name(self):
        return self.url

    def get_resolved_url(self):
        """
        Return usable URL.
        - direct path হলে সেটাই return করবে
        - named url হলে reverse করবে
        - invalid হলে empty string return করবে
        """
        raw = (self.url or "").strip()
        if not raw:
            return ""

        if raw.startswith("/"):
            return raw

        try:
            return reverse(raw)
        except NoReverseMatch:
            return ""

    def user_can_access(self, user):
        if not self.is_active:
            return False

        if not user.is_authenticated:
            return False

        if getattr(user, "is_superuser", False) or getattr(user, "is_admin", False):
            return True

        needed = [
            f"{app}.{code}"
            for app, code in self.permissions.values_list(
                "content_type__app_label",
                "codename",
            )
        ]

        if not needed:
            return True

        return any(user.has_perm(perm) for perm in needed)


class Roles(Common):
    name = models.CharField(max_length=50, unique=True, verbose_name="Role Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    menu = models.ManyToManyField(
        Menu,
        blank=True,
        related_name="role_menu_items",
        verbose_name="Menu Items",
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="custom_roles",
        verbose_name="Direct Permissions",
        help_text="Example: add_user, change_user, delete_user",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

# -------------------------
# USER MANAGER
# -------------------------

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", True)
        return self.create_user(email, password, **extra_fields)


class Branch(Common):
    name = models.CharField(max_length=100, verbose_name="Branch Name")
    address = models.TextField(verbose_name="Address")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    manager = models.ForeignKey(
        "Users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_branches",
        verbose_name="Manager",
    )
    branch_staff = models.ManyToManyField(
        "Users",
        blank=True,
        related_name="staffed_branches",
        verbose_name="Branch Staff",
    )
    total_area = models.ManyToManyField(
        "Area",
        blank=True,
        related_name="branches",
        verbose_name="Total Areas",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class Area(Common):
    name = models.CharField(max_length=100, verbose_name="Area Name")
    address = models.TextField(verbose_name="Address")
    parent_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="areas",
        null=True,
        blank=True,
        verbose_name="Branch",
    )
    area_staff = models.ManyToManyField(
        "Users",
        blank=True,
        related_name="staffed_areas",
        verbose_name="Area Staff",
    )
    total_customers = models.ManyToManyField(
        "CustomerGroup",
        blank=True,
        related_name="areas",
        verbose_name="Total Customer Groups",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    def __str__(self):
        return self.name


class CustomerGroup(Common):
    name = models.CharField(max_length=100, unique=True, verbose_name="Customer Group Name")
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer_groups",
        verbose_name="Branch",
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer_groups",
        verbose_name="Area",
    )
    customer_leader = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Customer Leader",
    )
    customer_group_staff = models.ManyToManyField(
        "Users",
        blank=True,
        related_name="staffed_customer_groups",
        verbose_name="Customer Group Staff",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Customer Group"
        verbose_name_plural = "Customer Groups"

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.area and self.branch and self.area.parent_branch_id != self.branch_id:
            raise ValidationError("Selected area does not belong to selected branch.")


class MultiBranch(Common):
    title = models.CharField(max_length=300)
    multi_branch = models.ManyToManyField(
        Branch,
        blank=True,
        related_name="multibranch_sets",
        verbose_name="Branches",
    )
    history = HistoricalRecords()

    class Meta:
        ordering = ["title"]
        verbose_name = "MultiBranch"
        verbose_name_plural = "MultiBranches"

    def __str__(self):
        return self.title


# -------------------------
# USER
# -------------------------

class Users(AbstractBaseUser, PermissionsMixin):
    status = models.BooleanField(default=True, null=True, blank=True, verbose_name="Active Status")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Created At")
    descriptions = RichTextField(null=True, blank=True, verbose_name="Descriptions")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, verbose_name="Deleted")

    name = models.CharField(max_length=100, default=None, null=True, blank=True, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    username = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="Username")

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Phone Number",
    )

    profile_picture = models.ImageField(upload_to="users/profile/", null=True, blank=True, verbose_name="Profile Picture")

    is_admin = models.BooleanField(default=False, verbose_name="Admin Status")
    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")
    is_verified = models.BooleanField(default=False, verbose_name="Verified")

    address = models.TextField(max_length=400, default=None, null=True, blank=True, verbose_name="Address")

    roles = models.ManyToManyField(Roles, blank=True, related_name="user_roles", verbose_name="Roles")

    nid_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="NID Number")
    nid_front = models.ImageField(upload_to="nid/front/", null=True, blank=True, verbose_name="NID Front Image")
    nid_back = models.ImageField(upload_to="nid/back/", null=True, blank=True, verbose_name="NID Back Images")

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Branch",
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_area",
        verbose_name="Area",
    )
    mult_branch = models.ManyToManyField(
        MultiBranch,
        blank=True,
        related_name="users_mult_branch",
        verbose_name="Multi Branch",
    )
    customer_group = models.ManyToManyField(
        CustomerGroup,
        blank=True,
        related_name="users_customer_group",
        verbose_name="Customer Group",
    )

    history = HistoricalRecords()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_role_permissions(self):
        if not self.is_authenticated:
            return set()

        perms = Permission.objects.filter(
            custom_roles__user_roles=self
        ).values_list("content_type__app_label", "codename")

        return {f"{app}.{code}" for app, code in perms}

    def get_menu_permissions(self):
        if not self.is_authenticated:
            return set()

        perms = Permission.objects.filter(
            sidebar_menus__role_menu_items__user_roles=self
        ).values_list("content_type__app_label", "codename").distinct()

        return {f"{app}.{code}" for app, code in perms}

    def get_all_permissions(self, obj=None):
        if self.is_admin or self.is_superuser:
            permissions = Permission.objects.values_list("content_type__app_label", "codename")
            return {f"{ct}.{name}" for ct, name in permissions}

        permissions = set()

        for role in self.roles.all():
            permissions.update(
                role.permissions.values_list("content_type__app_label", "codename")
            )
            for menu in role.menu.all():
                permissions.update(
                    menu.permissions.values_list("content_type__app_label", "codename")
                )

        return {f"{ct}.{name}" for ct, name in permissions}

    def has_perm(self, perm, obj=None):
        if self.is_admin or self.is_superuser:
            return True
        return perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        if self.is_superuser or getattr(self, "is_admin", False):
            return True
        return any(p.split(".")[0] == app_label for p in self.get_all_permissions())

    def sync_staff_relations(self):
        # Branch staff sync
        for branch in Branch.objects.filter(branch_staff=self):
            if self.branch_id != branch.id:
                branch.branch_staff.remove(self)

        if self.branch:
            self.branch.branch_staff.add(self)

        # Area staff sync
        for area in Area.objects.filter(area_staff=self):
            if self.area_id != area.id:
                area.area_staff.remove(self)

        if self.area:
            self.area.area_staff.add(self)
            if self.area.parent_branch and not self.branch_id:
                self.branch = self.area.parent_branch
                self.save(update_fields=["branch"])

        # Customer group staff sync
        selected_group_ids = set(self.customer_group.values_list("id", flat=True))

        for group in CustomerGroup.objects.filter(customer_group_staff=self):
            if group.id not in selected_group_ids:
                group.customer_group_staff.remove(self)

        for group in self.customer_group.all():
            group.customer_group_staff.add(self)

            changed = False
            if not group.branch_id and self.branch_id:
                group.branch = self.branch
                changed = True
            if not group.area_id and self.area_id:
                group.area = self.area
                changed = True
            if changed:
                group.save()


# -------------------------
# ACTIVITY LOG
# -------------------------

class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("role_update", "Role Update"),
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_actor",
    )
    target_user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_target",
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    app_label = models.CharField(max_length=100, null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        actor = self.user.email if self.user else "System"
        return f"{actor} - {self.action} - {self.model_name or ''}"



        