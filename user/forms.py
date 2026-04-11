


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.utils.html import format_html

from .models import Users, Roles, Branch, Area, MultiBranch, CustomerGroup, Menu

SELECT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-select"

MULTISELECT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-multiselect"
INPUT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:ring-orange-900"
TEXTAREA_CLASS = INPUT_CLASS + " min-h-[110px]"
SELECT_CLASS = INPUT_CLASS + " js-enhanced-select"
MULTISELECT_CLASS = INPUT_CLASS + " js-enhanced-multiselect"
CHECKBOX_CLASS = "h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500"


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• CUSTOM WIDGET WITH CREATE/EDIT BUTTONS â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
from django import forms
from django.utils.html import format_html


class RelatedSelectWidget(forms.Select):
    def __init__(self, model_name="", field_name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.field_name = field_name

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        existing_class = attrs.get("class", "")
        attrs["class"] = f"{existing_class} related-select-input".strip()

        select_html = super().render(name, value, attrs, renderer)

        if not self.model_name:
            return select_html

        buttons_html = format_html(
            '''
            <div class="related-action-buttons">
                <button type="button"
                        class="related-create-btn related-icon-btn related-icon-btn-create"
                        data-model="{}"
                        data-field-name="{}"
                        title="Create {}">
                    <i class="fas fa-plus"></i>
                </button>
                <button type="button"
                        class="related-edit-btn related-icon-btn related-icon-btn-edit"
                        data-model="{}"
                        data-field-name="{}"
                        title="Edit {}">
                    <i class="fas fa-pen"></i>
                </button>
            </div>
            ''',
            self.model_name, self.field_name, self.model_name.title(),
            self.model_name, self.field_name, self.model_name.title(),
        )

        return format_html(
            '''
            <div class="related-widget-wrap">
                <div class="related-widget-select">{}</div>
                {}
            </div>
            ''',
            select_html,
            buttons_html
        )


class RelatedMultiSelectWidget(forms.SelectMultiple):
    def __init__(self, model_name="", field_name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.field_name = field_name

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        existing_class = attrs.get("class", "")
        attrs["class"] = f"{existing_class} related-select-input".strip()

        select_html = super().render(name, value, attrs, renderer)

        if not self.model_name:
            return select_html

        buttons_html = format_html(
            '''
            <div class="related-action-buttons related-action-buttons-top">
                <button type="button"
                        class="related-create-btn related-icon-btn related-icon-btn-create"
                        data-model="{}"
                        data-field-name="{}"
                        title="Create {}">
                    <i class="fas fa-plus"></i>
                </button>
                <button type="button"
                        class="related-edit-btn related-icon-btn related-icon-btn-edit"
                        data-model="{}"
                        data-field-name="{}"
                        title="Edit {}">
                    <i class="fas fa-pen"></i>
                </button>
            </div>
            ''',
            self.model_name, self.field_name, self.model_name.title(),
            self.model_name, self.field_name, self.model_name.title(),
        )

        return format_html(
            '''
            <div class="related-widget-wrap related-widget-wrap-multi">
                <div class="related-widget-select">{}</div>
                {}
            </div>
            ''',
            select_html,
            buttons_html
        )


# class StyledModelForm(forms.ModelForm):
#     def apply_styles(self):
#         for name, field in self.fields.items():
#             widget = field.widget

#             if isinstance(widget, forms.Textarea):
#                 widget.attrs.setdefault("class", TEXTAREA_CLASS)
#             elif isinstance(widget, forms.Select) and not getattr(widget, "allow_multiple_selected", False):
#                 widget.attrs.setdefault("class", SELECT_CLASS)
#                 widget.attrs.setdefault("data-placeholder", f"Select {field.label}")
#             elif getattr(widget, "allow_multiple_selected", False):
#                 widget.attrs.setdefault("class", MULTISELECT_CLASS)
#                 widget.attrs.setdefault("data-placeholder", f"Select {field.label}")
#             elif isinstance(widget, forms.CheckboxInput):
#                 widget.attrs.setdefault("class", CHECKBOX_CLASS)
#             else:
#                 widget.attrs.setdefault("class", INPUT_CLASS)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_styles()


# class StyledModelForm(forms.ModelForm):
#     related_config = {}

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request", None)
#         super().__init__(*args, **kwargs)
#         self.apply_styles()

#     def _has_perm(self, perm_name: str) -> bool:
#         if not perm_name:
#             return False
#         user = getattr(self.request, "user", None)
#         if not user or not user.is_authenticated:
#             return False
#         return user.is_superuser or getattr(user, "is_admin", False) or user.has_perm(perm_name)

#     def apply_styles(self):
#         for name, field in self.fields.items():
#             widget = field.widget

#             if isinstance(widget, forms.Textarea):
#                 widget.attrs["class"] = TEXTAREA_CLASS

#             elif isinstance(widget, forms.CheckboxSelectMultiple):
#                 pass

#             elif isinstance(widget, forms.Select) and not getattr(widget, "allow_multiple_selected", False):
#                 widget.attrs["class"] = SELECT_CLASS
#                 widget.attrs.setdefault("data-placeholder", f"Select {field.label}")

#             elif getattr(widget, "allow_multiple_selected", False):
#                 widget.attrs["class"] = MULTISELECT_CLASS
#                 widget.attrs.setdefault("data-placeholder", f"Select {field.label}")

#             elif isinstance(widget, forms.CheckboxInput):
#                 widget.attrs["class"] = CHECKBOX_CLASS

#             else:
#                 widget.attrs["class"] = INPUT_CLASS

#             config = self.related_config.get(name)
#             if config:
#                 model_name = config.get("model", "")
#                 add_perm = config.get("can_add_perm", "")
#                 change_perm = config.get("can_change_perm", "")

#                 can_add = self._has_perm(add_perm)
#                 can_change = self._has_perm(change_perm)

#                 widget.attrs["data-related-model"] = model_name
#                 widget.attrs["data-can-add-perm"] = add_perm
#                 widget.attrs["data-can-change-perm"] = change_perm
#                 widget.attrs["data-parent-field"] = name

#                 widget.attrs["data_related_model"] = model_name
#                 widget.attrs["data_can_add_perm"] = add_perm
#                 widget.attrs["data_can_change_perm"] = change_perm
#                 widget.attrs["data_parent_field"] = name

#                 widget.attrs["can_add_related"] = can_add
#                 widget.attrs["can_change_related"] = can_change


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

    def apply_styles(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {TEXTAREA_CLASS}'.strip()

            elif isinstance(widget, forms.CheckboxSelectMultiple):
                pass

            elif isinstance(widget, forms.Select) and not getattr(widget, "allow_multiple_selected", False):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {SELECT_CLASS}'.strip()
                widget.attrs.setdefault("data-placeholder", f"Search {field.label}")
                widget.attrs.setdefault("data-width", "100%")
                widget.attrs.setdefault("data-allow-clear", "true")

            elif getattr(widget, "allow_multiple_selected", False):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {MULTISELECT_CLASS}'.strip()
                widget.attrs.setdefault("data-placeholder", f"Search {field.label}")
                widget.attrs.setdefault("data-width", "100%")

            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {CHECKBOX_CLASS}'.strip()

            else:
                widget.attrs["class"] = f'{widget.attrs.get("class", "")} {INPUT_CLASS}'.strip()

            config = self.related_config.get(name)
            if config and isinstance(widget, forms.Select):
                model_name = config.get("model") or config.get("model_name", "")
                add_perm = config.get("can_add_perm", "")
                change_perm = config.get("can_change_perm", "")

                can_add = self._has_perm(add_perm)
                can_change = self._has_perm(change_perm)

                widget.attrs["data-related-model"] = model_name
                widget.attrs["data-can-add-perm"] = add_perm
                widget.attrs["data-can-change-perm"] = change_perm
                widget.attrs["data-parent-field"] = name

                widget.attrs["data_related_model"] = model_name
                widget.attrs["data_can_add_perm"] = add_perm
                widget.attrs["data_can_change_perm"] = change_perm
                widget.attrs["data_parent_field"] = name

                widget.attrs["can_add_related"] = can_add
                widget.attrs["can_change_related"] = can_change

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
    )


from django.contrib.auth.models import Permission

class RoleForm(StyledModelForm):
    class Meta:
        model = Roles
        fields = ["name", "description", "menu", "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["menu"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")

        self.fields["permissions"].queryset = Permission.objects.select_related(
            "content_type"
        ).order_by("content_type__app_label", "codename")

        self.fields["permissions"].help_text = (
            "Select only what you want. Example: only change permission, or only delete permission."
        )

# class UserBaseForm(StyledModelForm):
#     related_config = {
#         "branch": {
#             "model": "branch",
#             "can_add_perm": "user.add_branch",
#             "can_change_perm": "user.change_branch",
#         },
#         "area": {
#             "model": "area",
#             "can_add_perm": "user.add_area",
#             "can_change_perm": "user.change_area",
#         },
#         "mult_branch": {
#             "model": "multibranch",
#             "can_add_perm": "user.add_multibranch",
#             "can_change_perm": "user.change_multibranch",
#         },
#         "customer_group": {
#             "model": "customergroup",
#             "can_add_perm": "user.add_customergroup",
#             "can_change_perm": "user.change_customergroup",
#         },
#         "roles": {
#             "model": "role",
#             "can_add_perm": "user.add_role",
#             "can_change_perm": "user.change_role",
#         },
#     }

#     password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
#     confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))

#     class Meta:
#         model = Users
#         fields = [
#             "name", "email", "username", "phone_number", "password", "confirm_password",
#             "profile_picture", "address", "descriptions", "nid_number", "nid_front", "nid_back",
#             "branch", "area", "mult_branch", "customer_group", "roles",
#             "status", "is_verified", "is_staff", "is_admin", "is_deleted",
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields["roles"].queryset = Roles.objects.order_by("name")
#         self.fields["branch"].queryset = Branch.objects.order_by("name")
#         self.fields["mult_branch"].queryset = MultiBranch.objects.order_by("title")

#         self.fields["area"].queryset = Area.objects.none()
#         self.fields["customer_group"].queryset = CustomerGroup.objects.none()

#         branch_id = None
#         area_id = None

#         if self.data.get("branch"):
#             branch_id = self.data.get("branch")
#         elif self.instance.pk and self.instance.branch_id:
#             branch_id = self.instance.branch_id

#         if self.data.get("area"):
#             area_id = self.data.get("area")
#         elif self.instance.pk and self.instance.area_id:
#             area_id = self.instance.area_id

#         if branch_id:
#             self.fields["area"].queryset = Area.objects.filter(
#                 parent_branch_id=branch_id
#             ).order_by("name")

#         cg_qs = CustomerGroup.objects.all().order_by("name")

#         if branch_id:
#             cg_qs = cg_qs.filter(branch_id=branch_id)

#         if area_id:
#             cg_qs = cg_qs.filter(area_id=area_id)

#         if branch_id or area_id:
#             self.fields["customer_group"].queryset = cg_qs

#     def clean(self):
#         cleaned = super().clean()

#         password = cleaned.get("password")
#         confirm_password = cleaned.get("confirm_password")

#         if password or confirm_password:
#             if password != confirm_password:
#                 raise forms.ValidationError("Password and confirm password must match.")

#         branch = cleaned.get("branch")
#         area = cleaned.get("area")
#         customer_groups = cleaned.get("customer_group")

#         if area and branch and area.parent_branch_id != branch.id:
#             self.add_error("area", "Selected area does not belong to the selected branch.")

#         if customer_groups:
#             invalid = []
#             for cg in customer_groups:
#                 if branch and cg.branch_id and cg.branch_id != branch.id:
#                     invalid.append(cg.name)
#                 if area and cg.area_id and cg.area_id != area.id:
#                     invalid.append(cg.name)

#             if invalid:
#                 self.add_error(
#                     "customer_group",
#                     f"Invalid customer group for selected branch/area: {', '.join(invalid)}"
#                 )

#         return cleaned

#     @transaction.atomic
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get("password")

#         if password:
#             user.set_password(password)

#         if commit:
#             user.save()
#             self.save_m2m()

#             if user.area:
#                 user.area.area_staf.add(user)

#             for cg in user.customer_group.all():
#                 cg.customer_group_Staff.add(user)

#             branch_updated = False
#             area_updated = False

#             if user.area and user.area.parent_branch and not user.branch:
#                 user.branch = user.area.parent_branch
#                 branch_updated = True

#             for cg in user.customer_group.all():
#                 if not user.branch and cg.branch:
#                     user.branch = cg.branch
#                     branch_updated = True
#                 if not user.area and cg.area:
#                     user.area = cg.area
#                     area_updated = True

#             if branch_updated or area_updated:
#                 update_fields = []
#                 if branch_updated:
#                     update_fields.append("branch")
#                 if area_updated:
#                     update_fields.append("area")
#                 user.save(update_fields=update_fields)

#             if user.branch:
#                 user.branch.branchStaff.add(user)

#             if user.area:
#                 user.area.area_staf.add(user)

#         return user


from django.contrib.auth.models import Permission

class UserBaseForm(StyledModelForm):
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
        "customer_group": {
            "model": "customergroup",
            "can_add_perm": "user.add_customergroup",
            "can_change_perm": "user.change_customergroup",
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

class UserCreateForm(UserBaseForm):
    pass


class UserUpdateForm(UserBaseForm):
    def clean(self):
        cleaned = super().clean()
        if not self.cleaned_data.get("password"):
            self.fields["password"].required = False
            self.fields["confirm_password"].required = False
        return cleaned


class UserForm(StyledModelForm):
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
        "roles": {
            "model": "role",
            "can_add_perm": "user.add_role",
            "can_change_perm": "user.change_role",
        },
    }

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Confirm Password"})
    )

    class Meta:
        model = Users
        fields = [
            "name",
            "email",
            "username",
            "phone_number",
            "branch",
            "area",
            "roles",
            "status",
            "is_staff",
            "is_admin",
            "profile_picture",
            "address",
        ]
        widgets = {
            "roles": forms.SelectMultiple(),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roles"].queryset = Roles.objects.order_by("name")
        self.fields["branch"].queryset = Branch.objects.order_by("name")
        self.fields["area"].queryset = Area.objects.none()

        branch_id = None
        if self.data.get("branch"):
            branch_id = self.data.get("branch")
        elif self.instance.pk and self.instance.branch_id:
            branch_id = self.instance.branch_id

        if branch_id:
            self.fields["area"].queryset = Area.objects.filter(parent_branch_id=branch_id).order_by("name")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if self.instance.pk:
            if password or confirm_password:
                if password != confirm_password:
                    raise forms.ValidationError("Passwords do not match.")
        else:
            if not password:
                raise forms.ValidationError("Password is required for new user.")
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        if commit:
            user.save()
            self.save_m2m()

        return user


class BranchQuickForm(StyledModelForm):
    class Meta:
        model = Branch
        fields = ["name", "phone", "manager", "branch_staff", "address", "total_area"]
        widgets = {
            "branch_staff": RelatedMultiSelectWidget(model_name="user", field_name="branch_staff"),
            "total_area": RelatedMultiSelectWidget(model_name="area", field_name="total_area"),
            "manager": RelatedSelectWidget(model_name="user", field_name="manager"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["manager"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")
        self.fields["branchStaff"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")
        self.fields["total_area"].queryset = Area.objects.order_by("name")

    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:
            obj.save()
            self.save_m2m()

            if obj.manager:
                obj.branchStaff.add(obj.manager)
                if obj.manager.branch_id != obj.id:
                    obj.manager.branch = obj
                    obj.manager.save(update_fields=["branch"])

            for area in obj.total_area.all():
                if area.parent_branch_id != obj.id:
                    area.parent_branch = obj
                    area.save(update_fields=["parent_branch"])

        return obj


class AreaQuickForm(StyledModelForm):
    class Meta:
        model = Area
        fields = ["name", "parent_branch", "area_staff", "address"]
        widgets = {
            "area_staff": RelatedMultiSelectWidget(model_name="user", field_name="area_staff"),
            "parent_branch": RelatedSelectWidget(model_name="branch", field_name="parent_branch"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent_branch"].queryset = Branch.objects.order_by("name")
        self.fields["area_staf"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")

    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:
            obj.save()
            self.save_m2m()

            if obj.parent_branch:
                obj.parent_branch.total_area.add(obj)
                for user in obj.area_staf.all():
                    if not user.branch_id:
                        user.branch = obj.parent_branch
                    user.area = obj
                    user.save(update_fields=["branch", "area"])

        return obj


from django import forms

class CustomerGroupQuickForm(StyledModelForm):
    customer_Leader = forms.ModelChoiceField(
        queryset=Users.objects.none(),
        required=False,
        widget=RelatedSelectWidget(model_name="user", field_name="customer_Leader"),
    )

    customer_group_Staff = forms.ModelMultipleChoiceField(
        queryset=Users.objects.none(),
        required=False,
        widget=RelatedMultiSelectWidget(model_name="user", field_name="customer_group_Staff"),
    )

    class Meta:
        model = CustomerGroup
        fields = [
            "name",
            "branch",
            "area",
            "customer_Leader",
            "customer_group_Staff",
            "description",
        ]
        widgets = {
            "branch": RelatedSelectWidget(model_name="branch", field_name="branch"),
            "area": RelatedSelectWidget(model_name="area", field_name="area"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["branch"].queryset = Branch.objects.order_by("name")
        self.fields["area"].queryset = Area.objects.select_related("parent_branch").order_by("name")
        self.fields["customer_Leader"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")
        self.fields["customer_group_Staff"].queryset = Users.objects.filter(is_deleted=False).order_by("name", "email")

        if self.instance.pk:
            # adjust these if your relations are stored differently
            if hasattr(self.instance, "customer_group_Staff"):
                self.fields["customer_group_Staff"].initial = self.instance.customer_group_Staff.all()

            if hasattr(self.instance, "customer_Leader"):
                self.fields["customer_Leader"].initial = self.instance.customer_Leader

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

            leader = self.cleaned_data.get("customer_Leader")
            staff_users = self.cleaned_data.get("customer_group_Staff")

            # If customer_group_Staff is a real M2M on CustomerGroup:
            if hasattr(obj, "customer_group_Staff"):
                obj.customer_group_Staff.set(staff_users)

            # If staff membership is actually stored on Users.customer_group:
            else:
                current_staff = Users.objects.filter(customer_group=obj)
                selected_ids = [u.id for u in staff_users]

                for user in current_staff.exclude(id__in=selected_ids):
                    user.customer_group.remove(obj)

                for user in staff_users:
                    if obj.branch and not user.branch_id:
                        user.branch = obj.branch
                    if obj.area and not user.area_id:
                        user.area = obj.area
                    user.save(update_fields=["branch", "area"])
                    user.customer_group.add(obj)

            # Only keep this if customer_Leader is a real field on CustomerGroup
            if hasattr(obj, "customer_Leader"):
                obj.customer_Leader = leader
                obj.save(update_fields=["customer_Leader"])

        return obj



class MultiBranchQuickForm(StyledModelForm):
    class Meta:
        model = MultiBranch
        fields = ["title", "multi_branch"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["multi_branch"].queryset = Branch.objects.order_by("name")


# class RoleQuickForm(StyledModelForm):
#     class Meta:
#         model = Roles
#         fields = ["name", "description", "menu"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["menu"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")


class RoleQuickForm(StyledModelForm):
    related_config = {
        "menu": {
            "model_name": "menu",
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


class MenuQuickForm(StyledModelForm):
    related_config = {
        "parent": {
            "model_name": "menu",
            "can_add_perm": "user.add_menu",
            "can_change_perm": "user.change_menu",
        },
    }

    class Meta:
        model = Menu
        fields = ["name", "url", "icon", "parent", "permissions"]
        widgets = {
            "permissions": forms.SelectMultiple(),
        }

# class MenuQuickForm(StyledModelForm):
#     class Meta:
#         model = Menu
#         fields = ["name", "icon", "url", "order", "is_active", "description", "parent", "permissions"]
#         widgets = {
#             "parent": RelatedSelectWidget(model_name="menu", field_name="parent"),
#             "permissions": RelatedMultiSelectWidget(model_name="permission", field_name="permissions"),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["parent"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")
#         self.fields["permissions"].queryset = Permission.objects.order_by("content_type__app_label", "codename")
    
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
            "parent": RelatedSelectWidget(model_name="menu", field_name="parent"),
            "permissions": forms.SelectMultiple(attrs={"class": MULTISELECT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Menu.objects.filter(is_active=True).order_by("order", "name")
        self.fields["permissions"].queryset = Permission.objects.select_related(
            "content_type"
        ).order_by("content_type__app_label", "codename")

# class UserQuickForm(StyledModelForm):
#     password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
#     confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))

#     class Meta:
#         model = Users
#         fields = [
#             "name",
#             "email",
#             "username",
#             "phone_number",
#             "branch",
#             "area",
#             "roles",
#             "status",
#             "is_staff",
#             "is_admin",
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields["roles"].queryset = Roles.objects.order_by("name")
#         self.fields["branch"].queryset = Branch.objects.order_by("name")
#         self.fields["area"].queryset = Area.objects.none()

#         branch_id = None

#         if self.data.get("branch"):
#             branch_id = self.data.get("branch")
#         elif self.instance.pk and self.instance.branch_id:
#             branch_id = self.instance.branch_id

#         if branch_id:
#             self.fields["area"].queryset = Area.objects.filter(
#                 parent_branch_id=branch_id
#             ).order_by("name")

#     def clean(self):
#         cleaned = super().clean()

#         password = cleaned.get("password")
#         confirm_password = cleaned.get("confirm_password")
#         branch = cleaned.get("branch")
#         area = cleaned.get("area")

#         if password or confirm_password:
#             if password != confirm_password:
#                 raise forms.ValidationError("Password and confirm password must match.")

#         if area and branch and area.parent_branch_id != branch.id:
#             self.add_error("area", "Selected area does not belong to the selected branch.")

#         return cleaned

#     def save(self, commit=True):
#         user = super().save(commit=False)

#         password = self.cleaned_data.get("password")
#         if password:
#             user.set_password(password)
#         elif not user.pk:
#             user.set_unusable_password()

#         if commit:
#             user.save()
#             self.save_m2m()

#         return user

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
    }

    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))

    class Meta:
        model = Users
        fields = [
            "name",
            "email",
            "username",
            "phone_number",
            "branch",
            "area",
            "roles",
            "status",
            "is_staff",
            "is_admin",
        ]
        widgets = {
            "roles": forms.SelectMultiple(attrs={"class": MULTISELECT_CLASS}),
        }





# from django import forms
# from .models import Branch, Area, CustomerGroup, Users
# SELECT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-select"

# MULTISELECT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-multiselect"
# INPUT_CLASS = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:focus:ring-orange-900"
# TEXTAREA_CLASS = INPUT_CLASS + " min-h-[110px]"
# SELECT_CLASS = INPUT_CLASS + " js-enhanced-select"
# MULTISELECT_CLASS = INPUT_CLASS + " js-enhanced-multiselect"
# CHECKBOX_CLASS = "h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500"
# from django.contrib.auth.forms import AuthenticationForm



# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(
#         widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email"})
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
#     )



# class BranchForm(forms.ModelForm):
#     class Meta:
#         model = Branch
#         fields = ["name", "address", "phone", "manager"]


# class AreaForm(forms.ModelForm):
#     class Meta:
#         model = Area
#         fields = ["name", "address", "parent_branch"]

#     def __init__(self, *args, **kwargs):
#         branch_id = kwargs.pop("branch_id", None)
#         super().__init__(*args, **kwargs)

#         if branch_id:
#             self.fields["parent_branch"].initial = branch_id


# class CustomerGroupForm(forms.ModelForm):
#     class Meta:
#         model = CustomerGroup
#         fields = ["name", "branch", "area", "customer_leader", "description"]

#     def __init__(self, *args, **kwargs):
#         branch_id = kwargs.pop("branch_id", None)
#         area_id = kwargs.pop("area_id", None)
#         super().__init__(*args, **kwargs)

#         if branch_id:
#             self.fields["branch"].initial = branch_id
#             self.fields["area"].queryset = Area.objects.filter(parent_branch_id=branch_id)
#         else:
#             self.fields["area"].queryset = Area.objects.all()

#         if area_id:
#             self.fields["area"].initial = area_id

#     def clean(self):
#         cleaned_data = super().clean()
#         branch = cleaned_data.get("branch")
#         area = cleaned_data.get("area")

#         if area and branch and area.parent_branch_id != branch.id:
#             raise forms.ValidationError("Selected area does not belong to selected branch.")

#         return cleaned_data


# class UserForm(forms.ModelForm):
#     password = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#     )

#     class Meta:
#         model = Users
#         fields = [
#             "name",
#             "email",
#             "username",
#             "password",
#             "phone_number",
#             "profile_picture",
#             "address",
#             "descriptions",
#             "roles",
#             "nid_number",
#             "nid_front",
#             "nid_back",
#             "branch",
#             "area",
#             "customer_group",
#             "mult_branch",
#             "status",
#             "is_admin",
#             "is_staff",
#             "is_verified",
#         ]
#         widgets = {
#             "customer_group": forms.SelectMultiple(attrs={"class": "form-control"}),
#             "roles": forms.SelectMultiple(attrs={"class": "form-control"}),
#             "mult_branch": forms.SelectMultiple(attrs={"class": "form-control"}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if field.widget.__class__.__name__ in ["TextInput", "EmailInput", "PasswordInput", "NumberInput", "FileInput", "ClearableFileInput"]:
#                 field.widget.attrs.update({"class": "form-control"})
#             elif field.widget.__class__.__name__ in ["Select", "SelectMultiple"]:
#                 field.widget.attrs.update({"class": "form-select"})
#             elif field.widget.__class__.__name__ == "Textarea":
#                 field.widget.attrs.update({"class": "form-control"})
#             elif field.widget.__class__.__name__ == "CheckboxInput":
#                 field.widget.attrs.update({"class": "form-check-input"})

#         self.fields["area"].queryset = Area.objects.none()
#         self.fields["customer_group"].queryset = CustomerGroup.objects.none()

#         # branch -> area
#         if "branch" in self.data:
#             try:
#                 branch_id = int(self.data.get("branch"))
#                 self.fields["area"].queryset = Area.objects.filter(parent_branch_id=branch_id)
#             except (ValueError, TypeError):
#                 self.fields["area"].queryset = Area.objects.none()
#         elif self.instance.pk and self.instance.branch:
#             self.fields["area"].queryset = Area.objects.filter(parent_branch=self.instance.branch)

#         # area -> customer group
#         if "area" in self.data:
#             try:
#                 area_id = int(self.data.get("area"))
#                 self.fields["customer_group"].queryset = CustomerGroup.objects.filter(area_id=area_id)
#             except (ValueError, TypeError):
#                 self.fields["customer_group"].queryset = CustomerGroup.objects.none()
#         elif self.instance.pk and self.instance.area:
#             self.fields["customer_group"].queryset = CustomerGroup.objects.filter(area=self.instance.area)

#     def clean(self):
#         cleaned_data = super().clean()
#         branch = cleaned_data.get("branch")
#         area = cleaned_data.get("area")
#         customer_groups = cleaned_data.get("customer_group")

#         if area and branch and area.parent_branch_id != branch.id:
#             raise forms.ValidationError("Selected area does not belong to selected branch.")

#         if customer_groups and area:
#             for cg in customer_groups:
#                 if cg.area_id != area.id:
#                     raise forms.ValidationError(
#                         f"Customer group '{cg.name}' does not belong to selected area."
#                     )

#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get("password")

#         if password:
#             user.set_password(password)

#         if commit:
#             user.save()
#             self.save_m2m()
#             user.sync_staff_relations()

#         return user






































































from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_class = "w-full rounded-2xl border px-4 py-3 pr-12 text-sm outline-none"

        self.fields["old_password"].widget.attrs.update({
            "class": common_class,
            "placeholder": "Enter current password",
            "style": "background:var(--surface-alt); border-color:var(--border); color:var(--text-main);",
        })
        self.fields["new_password1"].widget.attrs.update({
            "class": common_class,
            "placeholder": "Enter new password",
            "style": "background:var(--surface-alt); border-color:var(--border); color:var(--text-main);",
        })
        self.fields["new_password2"].widget.attrs.update({
            "class": common_class,
            "placeholder": "Confirm new password",
            "style": "background:var(--surface-alt); border-color:var(--border); color:var(--text-main);",
        })