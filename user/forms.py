


from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import Permission
from django.db import transaction

from user.scope import get_user_scope, is_global_user

from .models import Users, Roles, Branch, Area, MultiBranch, CustomerGroup, Menu


INPUT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:ring-orange-900"
TEXTAREA_CLASS = INPUT_CLASS + " min-h-[110px]"
SELECT_CLASS = INPUT_CLASS + " js-enhanced-select"
MULTISELECT_CLASS = INPUT_CLASS + " js-enhanced-multiselect"
CHECKBOX_CLASS = "h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500"



class StyledModelForm(forms.ModelForm):
    related_config = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.apply_styles()

    def _has_perm(self, perm_name: str) -> bool:
        if not perm_name:
            return False
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or getattr(user, "is_admin", False) or user.has_perm(perm_name)

    def _attach_manual_related_attrs(self, name, field, config):
        model_name = config.get("model") or config.get("model_name", "")
        add_perm = config.get("can_add_perm", "")
        change_perm = config.get("can_change_perm", "")

        field.widget.attrs["data_related_model"] = model_name
        field.widget.attrs["data_parent_field"] = name
        field.widget.attrs["can_add_related"] = self._has_perm(add_perm)
        field.widget.attrs["can_change_related"] = self._has_perm(change_perm)

    def _attach_auto_related_attrs(self, name, field):
        if not isinstance(field, (forms.ModelChoiceField, forms.ModelMultipleChoiceField)):
            return

        queryset = getattr(field, "queryset", None)
        target_model = getattr(queryset, "model", None)
        if not target_model:
            return

        model_name = target_model._meta.model_name
        if model_name in SKIP_AUTO_RELATED_MODELS:
            return

        route_model = get_route_model_name(target_model)
        if not route_model:
            return

        app_label = target_model._meta.app_label
        add_perm = f"{app_label}.add_{model_name}"
        change_perm = f"{app_label}.change_{model_name}"

        field.widget.attrs["data_related_model"] = route_model
        field.widget.attrs["data_parent_field"] = name
        field.widget.attrs["can_add_related"] = self._has_perm(add_perm)
        field.widget.attrs["can_change_related"] = self._has_perm(change_perm)

    def apply_styles(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {TEXTAREA_CLASS}'.strip()
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                pass
            elif getattr(widget, "allow_multiple_selected", False):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {MULTISELECT_CLASS}'.strip()
                widget.attrs.setdefault("data-placeholder", f"Search {field.label}")
                widget.attrs.setdefault("data-width", "100%")
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {SELECT_CLASS}'.strip()
                widget.attrs.setdefault("data-placeholder", f"Search {field.label}")
                widget.attrs.setdefault("data-width", "100%")
                widget.attrs.setdefault("data-allow-clear", "true")
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {CHECKBOX_CLASS}'.strip()
            else:
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {INPUT_CLASS}'.strip()

            # IMPORTANT: keep selected values for TomSelect
            if isinstance(field, forms.ModelChoiceField):
                if self.is_bound:
                    selected_value = self.data.get(name, "")
                else:
                    initial_value = self.initial.get(name, None)
                    if hasattr(initial_value, "pk"):
                        selected_value = initial_value.pk
                    elif initial_value not in (None, ""):
                        selected_value = initial_value
                    else:
                        selected_value = getattr(self.instance, f"{name}_id", "") if getattr(self, "instance", None) else ""

                widget.attrs["data-selected-value"] = str(selected_value or "")

            elif isinstance(field, forms.ModelMultipleChoiceField):
                if self.is_bound:
                    selected_values = self.data.getlist(name)
                else:
                    initial_value = self.initial.get(name, None)
                    if initial_value is not None:
                        if hasattr(initial_value, "values_list"):
                            selected_values = [str(v) for v in initial_value.values_list("pk", flat=True)]
                        else:
                            selected_values = [str(getattr(v, "pk", v)) for v in initial_value]
                    elif getattr(self, "instance", None) and getattr(self.instance, "pk", None):
                        manager = getattr(self.instance, name, None)
                        selected_values = [str(v) for v in manager.values_list("pk", flat=True)] if manager else []
                    else:
                        selected_values = []

                widget.attrs["data-selected-value"] = ",".join(selected_values)

            manual_config = self.related_config.get(name)
            if manual_config:
                self._attach_manual_related_attrs(name, field, manual_config)
            else:
                self._attach_auto_related_attrs(name, field)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))



class RoleQuickForm(StyledModelForm):
    related_config = {
        "menu": {
            "model": "menu",
            "can_add_perm": "user.add_menu",
            "can_change_perm": "user.change_menu",
        },
    }

    class Meta:
        model = Roles
        fields = ["name", "description", "menu", "permissions"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "menu": forms.SelectMultiple(),
            "permissions": forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["menu"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")
        self.fields["permissions"].queryset = Permission.objects.select_related("content_type").order_by(
            "content_type__app_label", "codename"
        )



class MenuQuickForm(StyledModelForm):
    related_config = {
        "parent": {
            "model": "menu",
            "can_add_perm": "user.add_menu",
            "can_change_perm": "user.change_menu",
        },
    }

    class Meta:
        model = Menu
        fields = ["name", "icon", "url", "order", "is_active", "description", "parent", "permissions"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "permissions": forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")
        self.fields["permissions"].queryset = Permission.objects.select_related("content_type").order_by(
            "content_type__app_label", "codename"
        )

class UserQuickForm(StyledModelForm):
    related_config = {
        "branch": {
            "model": "branch",
            "can_add_perm": "user.add_branch",
            "can_change_perm": "user.change_branch",
        },
        "area": {
            "model": "area",
            "can_add_perm": "user.add_area",
            "can_change_perm": "user.change_area",
        },
        "mult_branch": {
            "model": "multibranch",
            "can_add_perm": "user.add_multibranch",
            "can_change_perm": "user.change_multibranch",
        },
        "customer_group": {
            "model": "customergroup",
            "can_add_perm": "user.add_customergroup",
            "can_change_perm": "user.change_customergroup",
        },
        "roles": {
            "model": "role",
            "can_add_perm": "user.add_role",
            "can_change_perm": "user.change_role",
        },
    }

    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))

    class Meta:
        model = Users
        fields = [
            "name", "email", "username", "phone_number", "password", "confirm_password",
            "profile_picture", "address", "descriptions", "nid_number", "nid_front", "nid_back",
            "branch", "area", "mult_branch", "customer_group", "roles",
            "status", "is_verified", "is_staff", "is_admin", "is_deleted",
        ]
        widgets = {
            "roles": forms.SelectMultiple(),
            "mult_branch": forms.SelectMultiple(),
            "customer_group": forms.SelectMultiple(),
            "address": forms.Textarea(attrs={"rows": 3}),
            "descriptions": forms.Textarea(attrs={"rows": 4}),
        }

  
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     user = getattr(self.request, "user", None)
    #     scope = get_user_scope(user)

    #     self.fields["branch"].queryset = scope["branches"].order_by("name")
    #     self.fields["area"].queryset = scope["areas"].order_by("name")
    #     self.fields["customer_group"].queryset = scope["customer_groups"].order_by("name")
    #     self.fields["roles"].queryset = Roles.objects.order_by("name")

    #     if is_global_user(user):
    #         self.fields["mult_branch"].queryset = MultiBranch.objects.order_by("title")
    #     else:
    #         allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
    #         self.fields["mult_branch"].queryset = MultiBranch.objects.filter(
    #             multi_branch__id__in=allowed_branch_ids
    #         ).distinct().order_by("title")
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)

        branch_qs = scope["branches"]
        area_qs = scope["areas"]
        customer_group_qs = scope["customer_groups"]

        if self.instance.pk:
            if self.instance.branch_id:
                branch_qs = (branch_qs | Branch.objects.filter(pk=self.instance.branch_id)).distinct()

            if self.instance.area_id:
                area_qs = (area_qs | Area.objects.filter(pk=self.instance.area_id)).distinct()

            current_cg_ids = list(self.instance.customer_group.values_list("id", flat=True))
            if current_cg_ids:
                customer_group_qs = (customer_group_qs | CustomerGroup.objects.filter(pk__in=current_cg_ids)).distinct()

        self.fields["branch"].queryset = branch_qs.order_by("name")
        self.fields["area"].queryset = area_qs.order_by("name")
        self.fields["customer_group"].queryset = customer_group_qs.order_by("name")
        self.fields["roles"].queryset = Roles.objects.order_by("name")

        if is_global_user(user):
            self.fields["mult_branch"].queryset = MultiBranch.objects.order_by("title")
        else:
            allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
            self.fields["mult_branch"].queryset = MultiBranch.objects.filter(
                multi_branch__id__in=allowed_branch_ids
            ).distinct().order_by("title")

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")
        branch = cleaned.get("branch")
        area = cleaned.get("area")
        customer_groups = cleaned.get("customer_group")

        if self.instance.pk:
            if password or confirm_password:
                if password != confirm_password:
                    self.add_error("confirm_password", "Password and confirm password must match.")
        else:
            if not password:
                self.add_error("password", "Password is required for new user.")
            elif password != confirm_password:
                self.add_error("confirm_password", "Password and confirm password must match.")

        if area and not branch:
            cleaned["branch"] = area.parent_branch
            branch = cleaned["branch"]

        if area and branch and area.parent_branch_id != branch.id:
            self.add_error("area", "Selected area does not belong to the selected branch.")

        if customer_groups:
            invalid = []
            for cg in customer_groups:
                if branch and cg.branch_id and cg.branch_id != branch.id:
                    invalid.append(cg.name)
                if area and cg.area_id and cg.area_id != area.id:
                    invalid.append(cg.name)
            if invalid:
                self.add_error("customer_group", f"Invalid customer group for selected branch/area: {', '.join(invalid)}")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)
        elif not user.pk:
            user.set_unusable_password()

        if commit:
            user.save()
            self.save_m2m()
            user.sync_staff_relations()

        return user


class BranchQuickForm(StyledModelForm):
    related_config = {
        "manager": {
            "model": "user",
            "can_add_perm": "user.add_users",
            "can_change_perm": "user.change_users",
        },
        "branch_staff": {
            "model": "user",
            "can_add_perm": "user.add_users",
            "can_change_perm": "user.change_users",
        },
        "total_area": {
            "model": "area",
            "can_add_perm": "user.add_area",
            "can_change_perm": "user.change_area",
        },
    }

    class Meta:
        model = Branch
        fields = ["name", "phone", "manager", "branch_staff", "address", "total_area"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "branch_staff": forms.SelectMultiple(),
            "total_area": forms.SelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)

        users_qs = Users.objects.filter(is_deleted=False).order_by("name", "email")
        self.fields["manager"].queryset = users_qs
        self.fields["branch_staff"].queryset = users_qs
        self.fields["total_area"].queryset = scope["areas"].order_by("name")

        if self.instance.pk:
            self.fields["manager"].queryset = self.instance.branch_staff.all().order_by("name", "email")

    def clean(self):
        cleaned = super().clean()
        manager = cleaned.get("manager")
        branch_staff = cleaned.get("branch_staff")

        if manager and branch_staff is not None and manager not in branch_staff:
            # manager must be selected from branch staff; auto include
            cleaned["branch_staff"] = list(branch_staff) + [manager]

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:
            obj.save()
            self.save_m2m()

            if obj.manager:
                obj.branch_staff.add(obj.manager)
                if obj.manager.branch_id != obj.id:
                    obj.manager.branch = obj
                    obj.manager.save(update_fields=["branch"])

            for user in obj.branch_staff.all():
                if user.branch_id != obj.id:
                    user.branch = obj
                    user.save(update_fields=["branch"])

            for area in obj.total_area.all():
                if area.parent_branch_id != obj.id:
                    area.parent_branch = obj
                    area.save(update_fields=["parent_branch"])

        return obj


class AreaQuickForm(StyledModelForm):
    related_config = {
        "parent_branch": {
            "model": "branch",
            "can_add_perm": "user.add_branch",
            "can_change_perm": "user.change_branch",
        },
        "area_staff": {
            "model": "user",
            "can_add_perm": "user.add_users",
            "can_change_perm": "user.change_users",
        },
        "total_customers": {
            "model": "customergroup",
            "can_add_perm": "user.add_customergroup",
            "can_change_perm": "user.change_customergroup",
        },
    }

    class Meta:
        model = Area
        fields = ["name", "parent_branch", "area_staff", "total_customers", "address"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "area_staff": forms.SelectMultiple(),
            "total_customers": forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)

        self.fields["parent_branch"].queryset = scope["branches"].order_by("name")
        self.fields["area_staff"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")
        self.fields["total_customers"].queryset = scope["customer_groups"].order_by("name")


    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:
            obj.save()
            self.save_m2m()

            if obj.parent_branch:
                obj.parent_branch.total_area.add(obj)

            for user in obj.area_staff.all():
                changed = []
                if obj.parent_branch_id and user.branch_id != obj.parent_branch_id:
                    user.branch = obj.parent_branch
                    changed.append("branch")
                if user.area_id != obj.id:
                    user.area = obj
                    changed.append("area")
                if changed:
                    user.save(update_fields=changed)

            for cg in obj.total_customers.all():
                changed = False
                if cg.area_id != obj.id:
                    cg.area = obj
                    changed = True
                if obj.parent_branch_id and cg.branch_id != obj.parent_branch_id:
                    cg.branch = obj.parent_branch
                    changed = True
                if changed:
                    cg.save()

        return obj


class CustomerGroupQuickForm(StyledModelForm):
    related_config = {
        "branch": {
            "model": "branch",
            "can_add_perm": "user.add_branch",
            "can_change_perm": "user.change_branch",
        },
        "area": {
            "model": "area",
            "can_add_perm": "user.add_area",
            "can_change_perm": "user.change_area",
        },
        "customer_group_staff": {
            "model": "user",
            "can_add_perm": "user.add_users",
            "can_change_perm": "user.change_users",
        },
    }

    class Meta:
        model = CustomerGroup
        fields = ["name", "branch", "area", "customer_leader", "customer_group_staff", "description"]
        widgets = {
            "customer_leader": forms.TextInput(attrs={"placeholder": "Customer Leader Name"}),
            "customer_group_staff": forms.SelectMultiple(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)

        self.fields["branch"].queryset = scope["branches"].order_by("name")
        self.fields["area"].queryset = scope["areas"].order_by("name")
        self.fields["customer_group_staff"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")

    def clean(self):
        cleaned = super().clean()
        branch = cleaned.get("branch")
        area = cleaned.get("area")

        if area and not branch:
            cleaned["branch"] = area.parent_branch
            branch = cleaned["branch"]

        if area and branch and area.parent_branch_id != branch.id:
            self.add_error("area", "Selected area does not belong to the selected branch.")

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)

        if not obj.branch and obj.area:
            obj.branch = obj.area.parent_branch

        if commit:
            obj.save()
            self.save_m2m()

            for user in obj.customer_group_staff.all():
                changed = []
                if obj.branch_id and user.branch_id != obj.branch_id:
                    user.branch = obj.branch
                    changed.append("branch")
                if obj.area_id and user.area_id != obj.area_id:
                    user.area = obj.area
                    changed.append("area")
                if changed:
                    user.save(update_fields=changed)

            if obj.area:
                obj.area.total_customers.add(obj)

        return obj



class MultiBranchQuickForm(StyledModelForm):
    related_config = {
        "multi_branch": {
            "model": "branch",
            "can_add_perm": "user.add_branch",
            "can_change_perm": "user.change_branch",
        },
    }

    class Meta:
        model = MultiBranch
        fields = ["title", "multi_branch"]
        widgets = {
            "multi_branch": forms.SelectMultiple(),
        }

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)

        self.fields["multi_branch"].queryset = scope["branches"].order_by("name")

# aliases for existing imports/usages
RoleForm = RoleQuickForm
UserCreateForm = UserQuickForm
UserUpdateForm = UserQuickForm
UserForm = UserQuickForm


from django import forms

ROUTE_MODEL_ALIASES = {
    "users": "user",
    "roles": "role",
    "branch": "branch",
    "area": "area",
    "customergroup": "customergroup",
    "menu": "menu",
    "multibranch": "multibranch",
}

SKIP_AUTO_RELATED_MODELS = {
    "permission",
    "contenttype",
}


def get_route_model_name(model_cls):
    if not model_cls:
        return None
    return ROUTE_MODEL_ALIASES.get(model_cls._meta.model_name)



