import json
from datetime import datetime, timedelta
from multiprocessing import context
from multiprocessing import context
from urllib import request

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from product.forms import BrandForm, CategoryForm, UnickForm, UnitForm, WarrantyForm
from product.models import Brand, Category, Unit, Warranty, unick

from .scope import (
    get_multibranch_branch_ids,
    get_user_scope,
    
    apply_selected_filters,
    is_global_user,
)


from .forms import (
    AreaQuickForm,
    BranchQuickForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomerGroupQuickForm,
    MenuQuickForm,
    MultiBranchQuickForm,
    RoleForm,
    RoleQuickForm,
    UserQuickForm,
)
from .mixins import AdminRequiredMixin
from .models import ActivityLog, Area, Branch, CustomerGroup, Menu, MultiBranch, Roles, Users
from .utils import build_form_changes, build_snapshot_changes, log_activity


# -------------------------------------------------
# AUTH / DASHBOARD
# -------------------------------------------------
class HtmxListViewMixin:
    partial_template_name = None

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return [self.partial_template_name]
        return [self.template_name]


class CustomLoginView(DjangoLoginView):
    template_name = "auth/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        current_time = timezone.now()
        self.request.session["login_time"] = current_time.isoformat()
        log_activity(
            self.request,
            "login",
            f"{user} logged in at {current_time.strftime('%I:%M %p')}",
            target_user=user,
            obj=user,
        )
        messages.success(self.request, f"Welcome back, {user.name or user.email}!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url = "user:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.filter(is_deleted=False).count()
        context["total_roles"] = Roles.objects.count()
        context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:10]
        context["current_user"] = self.request.user
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    login_url = "user:login"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_name = request.user.name or request.user.email
            login_time = request.session.get("login_time")
            session_duration = "Unknown"

            if login_time:
                try:
                    login_dt = datetime.fromisoformat(login_time)
                    duration = timezone.now() - login_dt
                    minutes = int(duration.total_seconds() // 60)
                    seconds = int(duration.total_seconds() % 60)
                    session_duration = f"{minutes}m {seconds}s"
                except Exception:
                    session_duration = "N/A"

            log_activity(
                request,
                "logout",
                f"{request.user} logged out. Session duration: {session_duration}",
                target_user=request.user,
                obj=request.user,
            )
            logout(request)
            messages.success(request, f"Goodbye {user_name}! Session duration: {session_duration}")
        else:
            logout(request)

        return redirect("user:login")


# -------------------------------------------------
# HTMX PAGE HELPERS
# -------------------------------------------------

class HtmxTemplateView(LoginRequiredMixin, TemplateView):
    htmx_template_name = None
    normal_template_name = None
    login_url = "user:login"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return [self.htmx_template_name]
        return [self.normal_template_name]



class BaseNoTemplateDeleteView(LoginRequiredMixin, View):
    model = None
    success_url = None
    permission_required = ""
    success_message = "Deleted successfully."

    def has_delete_permission(self, request):
        return (
            request.user.is_authenticated and (
                request.user.is_superuser or
                getattr(request.user, "is_admin", False) or
                request.user.has_perm(self.permission_required)
            )
        )

    def cleanup_before_delete(self, obj):
        pass

    def post(self, request, pk, *args, **kwargs):
        if not self.has_delete_permission(request):
            if is_htmx(request):
                return HttpResponseForbidden("Permission denied")
            messages.error(request, "You don't have permission to delete this item.")
            return redirect(self.success_url)

        obj = get_object_or_404(self.model, pk=pk)
        label = str(obj)

        self.cleanup_before_delete(obj)
        obj.delete()

        log_activity(request, "delete", f"Deleted {label}", obj=obj)
        messages.success(request, self.success_message)

        if is_htmx(request):
            return htmx_trigger_response({
                "crud:deleted": {
                    "message": self.success_message,
                    "refreshList": True,
                }
            })

        return redirect(self.success_url)

class ProfilePageView(HtmxTemplateView):
    htmx_template_name = "user/userprofile/user_profile_main.html"
    normal_template_name = "user/userprofile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = (
            Users.objects.select_related("branch", "area")
            .prefetch_related("roles", "mult_branch", "customer_group")
            .get(pk=self.request.user.pk)
        )
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "user/userprofilepassword/change_password.html"
    success_url = reverse_lazy("profile_page")
    login_url = "user:login"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["user/userprofilepassword/change_password_main.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = (
            Users.objects.select_related("branch", "area")
            .prefetch_related("roles", "mult_branch", "customer_group")
            .get(pk=self.request.user.pk)
        )
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request"):
            messages.success(self.request, "Password changed successfully.")
            return render(
                self.request,
                "user/userprofilepassword/password_change_success.html",
                {"message": "Password changed successfully."},
            )
        return response


# -------------------------------------------------
# GENERIC HELPERS
# -------------------------------------------------

def normalize_model_name(model_name: str) -> str:
    model_name = (model_name or "").lower().strip()
    aliases = {
        "customer_group": "customergroup",
        "customergroups": "customergroup",
        "customer-group": "customergroup",
        "customergroup": "customergroup",
        "customergroup": "customergroup",
        "multi_branch": "multibranch",
        "multi-branch": "multibranch",
        "multibranches": "multibranch",
        "roles": "role",
        "users": "user",
    }
    return aliases.get(model_name, model_name)



import json
from django.http import HttpResponse
from django.contrib import messages

def is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def htmx_trigger_response(events: dict, status=204):
    response = HttpResponse("", status=status)
    response["HX-Trigger"] = json.dumps(events)
    return response


def object_label(obj):
    if hasattr(obj, "name") and obj.name:
        return obj.name
    if hasattr(obj, "title") and obj.title:
        return obj.title
    if hasattr(obj, "email") and obj.email:
        return obj.email
    return str(obj)


def compact_option(obj):
    return {
        "id": obj.pk,
        "text": object_label(obj),
    }

def user_has_permission(user, perm_name):
    return user.is_superuser or getattr(user, "is_admin", False) or user.has_perm(perm_name)


class PermissionRequiredViewMixin:
    required_permission = None
    denied_redirect = None
    denied_message = "You do not have permission to perform this action."

    def dispatch(self, request, *args, **kwargs):
        if self.required_permission and not user_has_permission(request.user, self.required_permission):
            messages.error(request, self.denied_message)
            return redirect(self.denied_redirect or "dashboard")
        return super().dispatch(request, *args, **kwargs)


class ScopedListContextMixin:
    def get_selected_filters(self):
        return {
            "branch": self.request.GET.get("branch", "").strip(),
            "area": self.request.GET.get("area", "").strip(),
            "customer_group": self.request.GET.get("customer_group", "").strip(),
        }

    def get_scope_context(self):
        selected = self.get_selected_filters()
        scope = get_user_scope(self.request.user)

        filtered = apply_selected_filters(
            scope["branches"],
            scope["areas"],
            scope["customer_groups"],
            selected_branch=selected["branch"],
            selected_area=selected["area"],
            selected_customer_group_ids=[selected["customer_group"]] if selected["customer_group"] else [],
        )

        return {
            "filter_branches": filtered["branches"].order_by("name"),
            "filter_areas": filtered["areas"].order_by("name"),
            "filter_customer_groups": filtered["customer_groups"].order_by("name"),
            "selected_branch": selected["branch"],
            "selected_area": selected["area"],
            "selected_customer_group": selected["customer_group"],
        }


class UserListView(LoginRequiredMixin, HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = Users
    template_name = "user/user_list.html"
    partial_template_name = "user/partials/user_list_content.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Users.objects.filter(is_deleted=False)
            .select_related("branch", "area")
            .prefetch_related("roles", "mult_branch", "customer_group")
        )

        user = self.request.user
        scope = get_user_scope(user)

        allowed_branch_ids = set(scope["branches"].values_list("id", flat=True))
        allowed_area_ids = set(scope["areas"].values_list("id", flat=True))
        allowed_customer_group_ids = set(scope["customer_groups"].values_list("id", flat=True))

        if not is_global_user(user):
            if allowed_customer_group_ids:
                queryset = queryset.filter(
                    Q(customer_group__id__in=allowed_customer_group_ids) |
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(area_id__in=allowed_area_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            elif allowed_area_ids:
                queryset = queryset.filter(
                    Q(area_id__in=allowed_area_ids) |
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            elif allowed_branch_ids:
                queryset = queryset.filter(
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            else:
                queryset = queryset.none()

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()
        customer_group_id = self.request.GET.get("customer_group", "").strip()
        role_id = self.request.GET.get("role", "").strip()
        created_from = self.request.GET.get("created_from", "").strip()
        created_to = self.request.GET.get("created_to", "").strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )

        if branch_id:
            queryset = queryset.filter(
                Q(branch_id=branch_id) |
                Q(mult_branch__multi_branch__id=branch_id)
            )

        if area_id:
            queryset = queryset.filter(area_id=area_id)

        if customer_group_id:
            queryset = queryset.filter(customer_group__id=customer_group_id)

        if role_id:
            queryset = queryset.filter(roles__id=role_id)

        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)

        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)

        return queryset.distinct().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_branch = self.request.GET.get("branch", "").strip()
        selected_area = self.request.GET.get("area", "").strip()
        selected_customer_group = self.request.GET.get("customer_group", "").strip()

        scope = get_user_scope(self.request.user)
        filtered = apply_selected_filters(
            scope["branches"],
            scope["areas"],
            scope["customer_groups"],
            selected_branch=selected_branch,
            selected_area=selected_area,
            selected_customer_group_ids=[selected_customer_group] if selected_customer_group else [],
        )

        context["branches"] = filtered["branches"].order_by("name")
        context["areas"] = filtered["areas"].order_by("name")
        context["customer_groups"] = filtered["customer_groups"].order_by("name")
        context["roles"] = Roles.objects.order_by("name")
        return context







class UserFormContextMixin:
    template_name = "user/user_form.html"
    success_url = reverse_lazy("user:user_list")

    def _sync_user_staff_links(self, user):
        if hasattr(user, "sync_staff_relations") and callable(user.sync_staff_relations):
            user.sync_staff_relations()
            return

        for branch in Branch.objects.filter(branch_staff=user):
            if user.branch_id != branch.id:
                branch.branch_staff.remove(user)

        for area in Area.objects.filter(area_staff=user):
            if user.area_id != area.id:
                area.area_staff.remove(user)

        selected_group_ids = set(user.customer_group.values_list("id", flat=True))
        for cg in CustomerGroup.objects.filter(customer_group_staff=user):
            if cg.id not in selected_group_ids:
                cg.customer_group_staff.remove(user)

        if user.area and user.area.parent_branch and not user.branch:
            user.branch = user.area.parent_branch
            user.save(update_fields=["branch"])

        for cg in user.customer_group.all():
            if not user.branch and cg.branch:
                user.branch = cg.branch
            if not user.area and cg.area:
                user.area = cg.area

        if user.branch_id or user.area_id:
            user.save(update_fields=["branch", "area"])

        if user.branch:
            user.branch.branch_staff.add(user)

        if user.area:
            user.area.area_staff.add(user)
            if user.area.parent_branch:
                user.area.parent_branch.total_area.add(user.area)

        for cg in user.customer_group.all():
            cg.customer_group_staff.add(user)
            if user.area:
                user.area.total_customers.add(cg)

    def get_common_context(self, request, obj=None, errors=None):
        selected_branch = request.POST.get("branch") or (str(obj.branch_id) if obj and obj.branch_id else "")
        selected_area = request.POST.get("area") or (str(obj.area_id) if obj and obj.area_id else "")

        if request.method == "POST":
            selected_role_ids = request.POST.getlist("roles")
            selected_mult_branch_ids = request.POST.getlist("mult_branch")
            selected_customer_group_ids = request.POST.getlist("customer_group")
        elif obj and obj.pk:
            selected_role_ids = [str(i) for i in obj.roles.values_list("id", flat=True)]
            selected_mult_branch_ids = [str(i) for i in obj.mult_branch.values_list("id", flat=True)]
            selected_customer_group_ids = [str(i) for i in obj.customer_group.values_list("id", flat=True)]
        else:
            selected_role_ids = []
            selected_mult_branch_ids = []
            selected_customer_group_ids = []

        scope = get_user_scope(request.user)

        filtered_scope = apply_selected_filters(
            scope["branches"],
            scope["areas"],
            scope["customer_groups"],
            selected_branch=selected_branch,
            selected_area=selected_area,
            selected_customer_group_ids=selected_customer_group_ids,
        )

        branches = filtered_scope["branches"].order_by("name")
        areas = filtered_scope["areas"].order_by("name")
        customer_groups = filtered_scope["customer_groups"].order_by("name")

        roles = Roles.objects.order_by("name")

        allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
        multibranches = MultiBranch.objects.prefetch_related("multi_branch").order_by("title")

        if not is_global_user(request.user):
            if allowed_branch_ids:
                multibranches = multibranches.filter(multi_branch__id__in=allowed_branch_ids).distinct()
            else:
                multibranches = multibranches.none()

        return {
            "object": obj,
            "errors": errors or {},
            "branches": branches,
            "areas": areas,
            "customer_groups": customer_groups,
            "roles": roles,
            "multibranches": multibranches,
            "selected_role_ids": selected_role_ids,
            "selected_mult_branch_ids": selected_mult_branch_ids,
            "selected_customer_group_ids": [str(i) for i in selected_customer_group_ids],
            "selected_branch": selected_branch,
            "selected_area": selected_area,
        }




class UserCreateView(LoginRequiredMixin, UserFormContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_common_context(request)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        errors = {}

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        address = request.POST.get("address", "").strip()
        descriptions = request.POST.get("descriptions", "").strip()
        nid_number = request.POST.get("nid_number", "").strip()

        branch_id = request.POST.get("branch") or None
        area_id = request.POST.get("area") or None

        role_ids = request.POST.getlist("roles")
        mult_branch_ids = request.POST.getlist("mult_branch")
        customer_group_ids = request.POST.getlist("customer_group")

        status = bool(request.POST.get("status"))
        is_verified = bool(request.POST.get("is_verified"))
        is_staff = bool(request.POST.get("is_staff"))
        is_admin = bool(request.POST.get("is_admin"))
        is_deleted = bool(request.POST.get("is_deleted"))

        profile_picture = request.FILES.get("profile_picture")
        nid_front = request.FILES.get("nid_front")
        nid_back = request.FILES.get("nid_back")

        if not email:
            errors["email"] = "Email is required."
        elif Users.objects.filter(email=email).exists():
            errors["email"] = "Email already exists."

        if username and Users.objects.filter(username=username).exists():
            errors["username"] = "Username already exists."

        if phone_number and Users.objects.filter(phone_number=phone_number).exists():
            errors["phone_number"] = "Phone number already exists."

        if not password:
            errors["password"] = "Password is required."

        if password != confirm_password:
            errors["confirm_password"] = "Password and confirm password must match."

        branch = Branch.objects.filter(pk=branch_id).first() if branch_id else None
        area = Area.objects.filter(pk=area_id).first() if area_id else None

        if area and branch and area.parent_branch_id != branch.id:
            errors["area"] = "Selected area does not belong to the selected branch."

        selected_customer_groups = CustomerGroup.objects.filter(id__in=customer_group_ids)
        invalid_customer_groups = []

        for cg in selected_customer_groups:
            if branch and cg.branch_id and cg.branch_id != branch.id:
                invalid_customer_groups.append(cg.name)
            if area and cg.area_id and cg.area_id != area.id:
                invalid_customer_groups.append(cg.name)

        if invalid_customer_groups:
            errors["customer_group"] = (
                "Invalid customer group for selected branch/area: " + ", ".join(invalid_customer_groups)
            )

        if errors:
            context = self.get_common_context(request, obj=None, errors=errors)
            return render(request, self.template_name, context)

        user = Users(
            name=name or None,
            email=email,
            username=username or None,
            phone_number=phone_number or None,
            address=address or None,
            descriptions=descriptions or None,
            nid_number=nid_number or None,
            branch=branch,
            area=area,
            status=status,
            is_verified=is_verified,
            is_staff=is_staff,
            is_admin=is_admin,
            is_deleted=is_deleted,
        )

        if profile_picture:
            user.profile_picture = profile_picture
        if nid_front:
            user.nid_front = nid_front
        if nid_back:
            user.nid_back = nid_back

        user.set_password(password)
        user.save()

        user.roles.set(Roles.objects.filter(id__in=role_ids))
        user.mult_branch.set(MultiBranch.objects.filter(id__in=mult_branch_ids))
        user.customer_group.set(selected_customer_groups)

        self._sync_user_staff_links(user)

        log_activity(request, "create", f"Created user {user.email}", target_user=user, obj=user)
        messages.success(request, "User created successfully.")
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, UserFormContextMixin, View):
    def get_object(self, pk):
        return get_object_or_404(Users, pk=pk, is_deleted=False)

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        context = self.get_common_context(request, obj=obj)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        errors = {}

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        address = request.POST.get("address", "").strip()
        descriptions = request.POST.get("descriptions", "").strip()
        nid_number = request.POST.get("nid_number", "").strip()

        branch_id = request.POST.get("branch") or None
        area_id = request.POST.get("area") or None

        role_ids = request.POST.getlist("roles")
        mult_branch_ids = request.POST.getlist("mult_branch")
        customer_group_ids = request.POST.getlist("customer_group")

        status = bool(request.POST.get("status"))
        is_verified = bool(request.POST.get("is_verified"))
        is_staff = bool(request.POST.get("is_staff"))
        is_admin = bool(request.POST.get("is_admin"))
        is_deleted = bool(request.POST.get("is_deleted"))

        profile_picture = request.FILES.get("profile_picture")
        nid_front = request.FILES.get("nid_front")
        nid_back = request.FILES.get("nid_back")

        if not email:
            errors["email"] = "Email is required."
        elif Users.objects.exclude(pk=obj.pk).filter(email=email).exists():
            errors["email"] = "Email already exists."

        if username and Users.objects.exclude(pk=obj.pk).filter(username=username).exists():
            errors["username"] = "Username already exists."

        if phone_number and Users.objects.exclude(pk=obj.pk).filter(phone_number=phone_number).exists():
            errors["phone_number"] = "Phone number already exists."

        if password or confirm_password:
            if password != confirm_password:
                errors["confirm_password"] = "Password and confirm password must match."

        branch = Branch.objects.filter(pk=branch_id).first() if branch_id else None
        area = Area.objects.filter(pk=area_id).first() if area_id else None

        if area and branch and area.parent_branch_id != branch.id:
            errors["area"] = "Selected area does not belong to the selected branch."

        selected_customer_groups = CustomerGroup.objects.filter(id__in=customer_group_ids)
        invalid_customer_groups = []

        for cg in selected_customer_groups:
            if branch and cg.branch_id and cg.branch_id != branch.id:
                invalid_customer_groups.append(cg.name)
            if area and cg.area_id and cg.area_id != area.id:
                invalid_customer_groups.append(cg.name)

        if invalid_customer_groups:
            errors["customer_group"] = (
                "Invalid customer group for selected branch/area: " + ", ".join(invalid_customer_groups)
            )

        if errors:
            context = self.get_common_context(request, obj=obj, errors=errors)
            return render(request, self.template_name, context)

        before_snapshot = {
            "name": obj.name,
            "email": obj.email,
            "username": obj.username,
            "phone_number": obj.phone_number,
            "address": obj.address,
            "descriptions": obj.descriptions,
            "nid_number": obj.nid_number,
            "branch": obj.branch,
            "area": obj.area,
            "status": obj.status,
            "is_verified": obj.is_verified,
            "is_staff": obj.is_staff,
            "is_admin": obj.is_admin,
            "is_deleted": obj.is_deleted,
            "roles": list(obj.roles.all()),
            "mult_branch": list(obj.mult_branch.all()),
            "customer_group": list(obj.customer_group.all()),
            "profile_picture": obj.profile_picture.name if obj.profile_picture else None,
            "nid_front": obj.nid_front.name if obj.nid_front else None,
            "nid_back": obj.nid_back.name if obj.nid_back else None,
        }

        obj.name = name or None
        obj.email = email
        obj.username = username or None
        obj.phone_number = phone_number or None
        obj.address = address or None
        obj.descriptions = descriptions or None
        obj.nid_number = nid_number or None
        obj.branch = branch
        obj.area = area
        obj.status = status
        obj.is_verified = is_verified
        obj.is_staff = is_staff
        obj.is_admin = is_admin
        obj.is_deleted = is_deleted

        if profile_picture:
            obj.profile_picture = profile_picture
        if nid_front:
            obj.nid_front = nid_front
        if nid_back:
            obj.nid_back = nid_back

        if password:
            obj.set_password(password)

        obj.save()

        obj.roles.set(Roles.objects.filter(id__in=role_ids))
        obj.mult_branch.set(MultiBranch.objects.filter(id__in=mult_branch_ids))
        obj.customer_group.set(selected_customer_groups)

        self._sync_user_staff_links(obj)

        after_snapshot = {
            "name": obj.name,
            "email": obj.email,
            "username": obj.username,
            "phone_number": obj.phone_number,
            "address": obj.address,
            "descriptions": obj.descriptions,
            "nid_number": obj.nid_number,
            "branch": obj.branch,
            "area": obj.area,
            "status": obj.status,
            "is_verified": obj.is_verified,
            "is_staff": obj.is_staff,
            "is_admin": obj.is_admin,
            "is_deleted": obj.is_deleted,
            "roles": list(obj.roles.all()),
            "mult_branch": list(obj.mult_branch.all()),
            "customer_group": list(obj.customer_group.all()),
            "profile_picture": obj.profile_picture.name if obj.profile_picture else None,
            "nid_front": obj.nid_front.name if obj.nid_front else None,
            "nid_back": obj.nid_back.name if obj.nid_back else None,
        }

        changes = build_snapshot_changes(
            before_snapshot,
            after_snapshot,
            labels={
                "name": "Name",
                "email": "Email",
                "username": "Username",
                "phone_number": "Phone Number",
                "address": "Address",
                "descriptions": "Description",
                "nid_number": "NID Number",
                "branch": "Branch",
                "area": "Area",
                "status": "Status",
                "is_verified": "Verified",
                "is_staff": "Staff",
                "is_admin": "Admin",
                "is_deleted": "Deleted",
                "roles": "Roles",
                "mult_branch": "Multi Branch",
                "customer_group": "Customer Group",
                "profile_picture": "Profile Picture",
                "nid_front": "NID Front",
                "nid_back": "NID Back",
            },
        )

        log_activity(
            request,
            "update",
            f"Updated user {obj.email}",
            target_user=obj,
            obj=obj,
            changes=changes,
        )
        messages.success(request, "User updated successfully.")
        return redirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, PermissionRequiredViewMixin, DeleteView):
    model = Users
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("user:user_list")
    required_permission = "user.delete_users"
    denied_redirect = "user:user_list"
    denied_message = "You do not have permission to delete users."

    def form_valid(self, form):
        user = self.get_object()
        user.is_deleted = True
        user.save(update_fields=["is_deleted"])
        log_activity(self.request, "delete", f"Soft deleted user {user.email}", target_user=user, obj=user)
        messages.success(self.request, "User deleted successfully.")
        if is_htmx(self.request):
            return htmx_trigger_response({
                "crud:deleted": {
                    "message": "User deleted successfully.",
                    "refreshList": True,
                }
            })
        return redirect(self.success_url)


# -------------------------------------------------
# ROLE CRUD
# -------------------------------------------------

class RoleListView(LoginRequiredMixin, HtmxListViewMixin, ListView):
    model = Roles
    template_name = "user/role_list.html"
    partial_template_name = "user/partials/role_list_content.html"
    context_object_name = "roles"

    def get_queryset(self):
        return Roles.objects.prefetch_related("permissions", "user_roles", "menu").all()


class RoleCreateView(LoginRequiredMixin, PermissionRequiredViewMixin, CreateView):
    model = Roles
    form_class = RoleForm
    template_name = "user/role_form.html"
    success_url = reverse_lazy("user:role_list")
    required_permission = "user.add_role"
    denied_redirect = "user:role_list"
    denied_message = "You do not have permission to create roles."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request, "role_update", f"Created role {self.object.name}", obj=self.object)
        messages.success(self.request, "Role created successfully.")
        return response


class RoleUpdateView(LoginRequiredMixin, PermissionRequiredViewMixin, UpdateView):
    model = Roles
    form_class = RoleForm
    template_name = "user/role_form.html"
    success_url = reverse_lazy("user:role_list")
    required_permission = "user.change_role"
    denied_redirect = "user:role_list"
    denied_message = "You do not have permission to update roles."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        changes = build_form_changes(form)
        response = super().form_valid(form)
        log_activity(
            self.request,
            "role_update",
            f"Updated role {self.object.name}",
            obj=self.object,
            changes=changes,
        )
        messages.success(self.request, "Role updated successfully.")
        return response


class RoleDeleteView(BaseNoTemplateDeleteView):
    model = Roles
    success_url = reverse_lazy("user:role_list")
    permission_required = "user.delete_role"
    success_message = "Role deleted successfully."


class BranchListView(LoginRequiredMixin, HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = Branch
    template_name = "user/branch_list.html"
    partial_template_name = "user/partials/branch_list_content.html"
    context_object_name = "branches"

    def get_queryset(self):
        qs = get_user_scope(self.request.user)["branches"].select_related("manager").prefetch_related(
            "branch_staff", "total_area"
        )

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(phone__icontains=search)
            )

        if branch_id:
            qs = qs.filter(id=branch_id)

        return qs.distinct().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_scope_context())
        return context

class ScopedListContextMixin:
    def get_selected_filters(self):
        return {
            "branch": self.request.GET.get("branch", "").strip(),
            "area": self.request.GET.get("area", "").strip(),
            "customer_group": self.request.GET.get("customer_group", "").strip(),
        }

    def get_scope_context(self):
        selected = self.get_selected_filters()
        scope = get_user_scope(self.request.user)

        filtered = apply_selected_filters(
            scope["branches"],
            scope["areas"],
            scope["customer_groups"],
            selected_branch=selected["branch"],
            selected_area=selected["area"],
            selected_customer_group_ids=[selected["customer_group"]] if selected["customer_group"] else [],
        )

        return {
            "filter_branches": filtered["branches"].order_by("name"),
            "filter_areas": filtered["areas"].order_by("name"),
            "filter_customer_groups": filtered["customer_groups"].order_by("name"),
            "selected_branch": selected["branch"],
            "selected_area": selected["area"],
            "selected_customer_group": selected["customer_group"],
        }




class AreaListView(LoginRequiredMixin,HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = Area
    template_name = "user/area_list.html"
    partial_template_name = "user/partials/area_list_content.html"
    context_object_name = "areas"

    def get_queryset(self):
        qs = (
            get_user_scope(self.request.user)["areas"]
            .select_related("parent_branch")
            .prefetch_related("area_staff", "total_customers")
        )

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()

        if branch_id:
            qs = qs.filter(parent_branch_id=branch_id)

        if area_id:
            qs = qs.filter(id=area_id)

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(parent_branch__name__icontains=search)
            )

        return qs.distinct().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_scope_context())
        context["selected_search"] = self.request.GET.get("search", "").strip()
        return context
    

class AreaListView(LoginRequiredMixin,HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = Area
    template_name = "user/area_list.html"
    partial_template_name = "user/partials/area_list_content.html"
    context_object_name = "areas"

    def get_queryset(self):
        qs = (
            get_user_scope(self.request.user)["areas"]
            .select_related("parent_branch")
            .prefetch_related("area_staff", "total_customers")
        )

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()

        if branch_id:
            qs = qs.filter(parent_branch_id=branch_id)

        if area_id:
            qs = qs.filter(id=area_id)

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(parent_branch__name__icontains=search)
            )

        return qs.distinct().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_scope_context())
        context["selected_search"] = self.request.GET.get("search", "").strip()
        return context


class CustomerGroupListView(LoginRequiredMixin,HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = CustomerGroup
    template_name = "user/customer_group_list.html"
    partial_template_name = "user/partials/customer_group_list_content.html"
    context_object_name = "customer_groups"

    def get_queryset(self):
        qs = (
            get_user_scope(self.request.user)["customer_groups"]
            .select_related("branch", "area")
            .prefetch_related("customer_group_staff")
        )

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()
        customer_group_id = self.request.GET.get("customer_group", "").strip()

        if branch_id:
            qs = qs.filter(branch_id=branch_id)

        if area_id:
            qs = qs.filter(area_id=area_id)

        if customer_group_id:
            qs = qs.filter(id=customer_group_id)

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(branch__name__icontains=search) |
                Q(area__name__icontains=search)
            )

        return qs.distinct().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_scope_context())
        context["selected_search"] = self.request.GET.get("search", "").strip()
        return context
class MenuListView(LoginRequiredMixin, HtmxListViewMixin, ListView):
    model = Menu
    template_name = "user/menu_list.html"
    partial_template_name = "user/partials/menu_list_content.html"
    context_object_name = "menus"

    def get_queryset(self):
        qs = (
            Menu.objects.select_related("parent")
            .prefetch_related("permissions", "role_menu_items")
            .order_by("order", "name")
        )

        search = self.request.GET.get("search", "").strip()
        status = self.request.GET.get("status", "").strip()
        parent_id = self.request.GET.get("parent", "").strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(url__icontains=search) |
                Q(icon__icontains=search) |
                Q(description__icontains=search) |
                Q(parent__name__icontains=search)
            )

        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)

        if parent_id == "root":
            qs = qs.filter(parent__isnull=True)
        elif parent_id:
            qs = qs.filter(parent_id=parent_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parents"] = Menu.objects.order_by("name")
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["selected_status"] = self.request.GET.get("status", "").strip()
        context["selected_parent"] = self.request.GET.get("parent", "").strip()
        return context


class MultiBranchListView(LoginRequiredMixin, HtmxListViewMixin, ScopedListContextMixin, ListView):
    model = MultiBranch
    template_name = "user/multibranch_list.html"
    partial_template_name = "user/partials/multibranch_list_content.html"
    context_object_name = "multibranches"

    def get_queryset(self):
        qs = MultiBranch.objects.prefetch_related("multi_branch", "users_mult_branch")

        user = self.request.user
        scope = get_user_scope(user)
        allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))

        if not is_global_user(user):
            if allowed_branch_ids:
                qs = qs.filter(multi_branch__id__in=allowed_branch_ids)
            else:
                qs = qs.none()

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()

        if branch_id:
            qs = qs.filter(multi_branch__id=branch_id)

        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(multi_branch__name__icontains=search)
            )

        return qs.distinct().order_by("title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_scope_context())
        context["selected_search"] = self.request.GET.get("search", "").strip()
        return context





class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = "user/activity_log.html"
    context_object_name = "logs"
    paginate_by = 20

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            hx_target = (self.request.headers.get("HX-Target", "") or "").lstrip("#")

            # filter/pagination request
            if hx_target == "activity-log-results":
                return ["user/partials/activity_log_table.html"]

            # sidebar/menu first click request
            return ["user/partials/activity_log_page.html"]

        return ["user/activity_log.html"]

    def get_queryset(self):
        queryset = (
            ActivityLog.objects
            .select_related("user", "target_user", "user__branch", "user__area")
            .prefetch_related("user__customer_group")
            .order_by("-created_at")
        )

        scope = get_user_scope(self.request.user)
        allowed_branch_ids = set(scope["branches"].values_list("id", flat=True))
        allowed_area_ids = set(scope["areas"].values_list("id", flat=True))
        allowed_customer_group_ids = set(scope["customer_groups"].values_list("id", flat=True))

        if not is_global_user(self.request.user):
            if allowed_customer_group_ids:
                queryset = queryset.filter(
                    Q(user__customer_group__id__in=allowed_customer_group_ids) |
                    Q(user__branch_id__in=allowed_branch_ids) |
                    Q(user__area_id__in=allowed_area_ids)
                )
            elif allowed_area_ids:
                queryset = queryset.filter(
                    Q(user__area_id__in=allowed_area_ids) |
                    Q(user__branch_id__in=allowed_branch_ids)
                )
            elif allowed_branch_ids:
                queryset = queryset.filter(user__branch_id__in=allowed_branch_ids)
            else:
                queryset = queryset.none()

        search = self.request.GET.get("search", "").strip()
        user_id = self.request.GET.get("user", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()
        customer_group_id = self.request.GET.get("customer_group", "").strip()
        action = self.request.GET.get("action", "").strip()
        from_date = self.request.GET.get("from_date", "").strip()
        to_date = self.request.GET.get("to_date", "").strip()

        if search:
            search_filter = (
                Q(description__icontains=search) |
                Q(user__name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(model_name__icontains=search) |
                Q(object_repr__icontains=search) |
                Q(target_user__name__icontains=search) |
                Q(target_user__email__icontains=search)
            )

            if search.isdigit():
                search_filter |= Q(object_id=int(search))

            queryset = queryset.filter(search_filter)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if branch_id:
            queryset = queryset.filter(user__branch_id=branch_id)

        if area_id:
            queryset = queryset.filter(user__area_id=area_id)

        if customer_group_id:
            queryset = queryset.filter(user__customer_group__id=customer_group_id)

        if action:
            queryset = queryset.filter(action=action)

        if from_date:
            queryset = queryset.filter(created_at__date__gte=from_date)

        if to_date:
            queryset = queryset.filter(created_at__date__lte=to_date)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_search = self.request.GET.get("search", "").strip()
        selected_user = self.request.GET.get("user", "").strip()
        selected_branch = self.request.GET.get("branch", "").strip()
        selected_area = self.request.GET.get("area", "").strip()
        selected_customer_group = self.request.GET.get("customer_group", "").strip()
        selected_action = self.request.GET.get("action", "").strip()
        selected_from_date = self.request.GET.get("from_date", "").strip()
        selected_to_date = self.request.GET.get("to_date", "").strip()

        scope = get_user_scope(self.request.user)
        filtered_scope = apply_selected_filters(
            scope["branches"],
            scope["areas"],
            scope["customer_groups"],
            selected_branch=selected_branch,
            selected_area=selected_area,
            selected_customer_group_ids=[selected_customer_group] if selected_customer_group else [],
        )

        context["branches"] = filtered_scope["branches"].order_by("name")
        context["areas"] = filtered_scope["areas"].order_by("name")
        context["customer_groups"] = filtered_scope["customer_groups"].order_by("name")

        allowed_branch_ids = set(scope["branches"].values_list("id", flat=True))
        allowed_area_ids = set(scope["areas"].values_list("id", flat=True))
        allowed_customer_group_ids = set(scope["customer_groups"].values_list("id", flat=True))
        users_qs = Users.objects.filter(is_deleted=False)

        if not is_global_user(self.request.user):
            if allowed_customer_group_ids:
                users_qs = users_qs.filter(
                    Q(customer_group__id__in=allowed_customer_group_ids) |
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(area_id__in=allowed_area_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            elif allowed_area_ids:
                users_qs = users_qs.filter(
                    Q(area_id__in=allowed_area_ids) |
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            elif allowed_branch_ids:
                users_qs = users_qs.filter(
                    Q(branch_id__in=allowed_branch_ids) |
                    Q(mult_branch__multi_branch__id__in=allowed_branch_ids)
                )
            else:
                users_qs = users_qs.none()

        context["users"] = users_qs.distinct().order_by("name")

        today = timezone.localdate()
        base_qs = ActivityLog.objects.all()
        context["today_count"] = base_qs.filter(created_at__date=today).count()
        context["week_count"] = base_qs.filter(created_at__date__gte=today - timedelta(days=7)).count()
        context["month_count"] = base_qs.filter(created_at__date__gte=today - timedelta(days=30)).count()

        context["action_choices"] = ActivityLog.ACTION_CHOICES
        context["selected_search"] = selected_search
        context["selected_user"] = selected_user
        context["selected_branch"] = selected_branch
        context["selected_area"] = selected_area
        context["selected_customer_group"] = selected_customer_group
        context["selected_action"] = selected_action
        context["selected_from_date"] = selected_from_date
        context["selected_to_date"] = selected_to_date

        return context



# -------------------------------------------------
# MODEL DELETE VIEWS
# -------------------------------------------------

class BranchDeleteView(BaseNoTemplateDeleteView):
    model = Branch
    success_url = reverse_lazy("user:branch_list")
    permission_required = "user.delete_branch"
    success_message = "Branch deleted successfully."

    def cleanup_before_delete(self, obj):
        obj.branch_staff.clear()
        obj.total_area.clear()


class AreaDeleteView(BaseNoTemplateDeleteView):
    model = Area
    success_url = reverse_lazy("user:area_list")
    permission_required = "user.delete_area"
    success_message = "Area deleted successfully."

    def cleanup_before_delete(self, obj):
        obj.area_staff.clear()
        obj.total_customers.clear()


class CustomerGroupDeleteView(BaseNoTemplateDeleteView):
    model = CustomerGroup
    success_url = reverse_lazy("user:customer_group_list")
    permission_required = "user.delete_customergroup"
    success_message = "Customer group deleted successfully."

    def cleanup_before_delete(self, obj):
        obj.customer_group_staff.clear()


class MenuDeleteView(BaseNoTemplateDeleteView):
    model = Menu
    success_url = reverse_lazy("user:menu_list")
    permission_required = "user.delete_menu"
    success_message = "Menu deleted successfully."

    def cleanup_before_delete(self, obj):
        obj.role_menu_items.clear()
        Menu.objects.filter(parent=obj).update(parent=None)


class MultiBranchDeleteView(BaseNoTemplateDeleteView):
    model = MultiBranch
    success_url = reverse_lazy("user:multibranch_list")
    permission_required = "user.delete_multibranch"
    success_message = "MultiBranch deleted successfully."

    def cleanup_before_delete(self, obj):
        obj.multi_branch.clear()


# -------------------------------------------------
# HTMX RELATED MODAL + AJAX
# -------------------------------------------------

MODEL_FORM_MAP = {
    "branch": (Branch, BranchQuickForm),
    "area": (Area, AreaQuickForm),
    "customergroup": (CustomerGroup, CustomerGroupQuickForm),
    "multibranch": (MultiBranch, MultiBranchQuickForm),
    "role": (Roles, RoleQuickForm),
    "menu": (Menu, MenuQuickForm),
    "user": (Users, UserQuickForm),
}

MODEL_PERMISSION_MAP = {
    "branch": ("user.add_branch", "user.change_branch"),
    "area": ("user.add_area", "user.change_area"),
    "customergroup": ("user.add_customergroup", "user.change_customergroup"),
    "multibranch": ("user.add_multibranch", "user.change_multibranch"),
    "role": ("user.add_role", "user.change_role"),
    "menu": ("user.add_menu", "user.change_menu"),
    "user": ("user.add_users", "user.change_users"),
}





from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from .scope import get_user_scope


def compact_option(obj):
    if hasattr(obj, "name") and obj.name:
        text = obj.name
    elif hasattr(obj, "title") and obj.title:
        text = obj.title
    elif hasattr(obj, "email") and obj.email:
        text = obj.email
    else:
        text = str(obj)

    return {
        "id": obj.pk,
        "text": text,
    }

@login_required
@require_GET
def ajax_areas_by_branch(request):
    branch_id = request.GET.get("branch_id", "").strip()
    scope = get_user_scope(request.user)

    qs = scope["areas"]
    if branch_id:
        qs = qs.filter(parent_branch_id=branch_id)

    return JsonResponse({
        "results": [compact_option(obj) for obj in qs.distinct().order_by("name")]
    })


@login_required
@require_GET
def ajax_customer_groups(request):
    branch_id = request.GET.get("branch_id", "").strip()
    area_id = request.GET.get("area_id", "").strip()

    scope = get_user_scope(request.user)
    qs = scope["customer_groups"]

    if branch_id:
        qs = qs.filter(branch_id=branch_id)

    if area_id:
        qs = qs.filter(area_id=area_id)

    return JsonResponse({
        "results": [compact_option(obj) for obj in qs.distinct().order_by("name")]
    })


@login_required
@require_GET
def ajax_branch_meta(request, pk):
    branch = get_object_or_404(
        Branch.objects.prefetch_related("branch_staff", "total_area"),
        pk=pk,
    )
    return JsonResponse(
        {
            "id": branch.id,
            "manager_id": branch.manager_id,
            "staff_ids": list(branch.branch_staff.values_list("id", flat=True)),
            "area_ids": list(branch.total_area.values_list("id", flat=True)),
        }
    )


@login_required
@require_GET
def ajax_area_meta(request, pk):
    area = get_object_or_404(
        Area.objects.prefetch_related("area_staff", "total_customers"),
        pk=pk,
    )
    return JsonResponse(
        {
            "id": area.id,
            "branch_id": area.parent_branch_id,
            "staff_ids": list(area.area_staff.values_list("id", flat=True)),
            "customer_group_ids": list(area.total_customers.values_list("id", flat=True)),
        }
    )
# @login_required
# @require_http_methods(["GET", "POST"])
# def related_object_modal(request, model_name, pk=None):
#     model_name = normalize_model_name(model_name)

#     MODEL_CONFIG = {
#         "branch": {
#             "model": Branch,
#             "form": BranchQuickForm,
#             "permission_add": "user.add_branch",
#             "permission_change": "user.change_branch",
#         },
#         "area": {
#             "model": Area,
#             "form": AreaQuickForm,
#             "permission_add": "user.add_area",
#             "permission_change": "user.change_area",
#         },
#         "customergroup": {
#             "model": CustomerGroup,
#             "form": CustomerGroupQuickForm,
#             "permission_add": "user.add_customergroup",
#             "permission_change": "user.change_customergroup",
#         },
#         "multibranch": {
#             "model": MultiBranch,
#             "form": MultiBranchQuickForm,
#             "permission_add": "user.add_multibranch",
#             "permission_change": "user.change_multibranch",
#         },
#         "role": {
#             "model": Roles,
#             "form": RoleQuickForm,
#             "permission_add": "user.add_role",
#             "permission_change": "user.change_role",
#         },
#         "user": {
#             "model": Users,
#             "form": UserQuickForm,
#             "permission_add": "user.add_users",
#             "permission_change": "user.change_users",
#         },
#         "menu": {
#             "model": Menu,
#             "form": MenuQuickForm,
#             "permission_add": "user.add_menu",
#             "permission_change": "user.change_menu",
#         },

        
#     }

#     if model_name not in MODEL_CONFIG:
#         return HttpResponse("Invalid model.", status=400)

#     config = MODEL_CONFIG[model_name]
#     model_class = config["model"]
#     form_class = config["form"]

#     instance = get_object_or_404(model_class, pk=pk) if pk else None

#     permission_name = config["permission_change"] if instance else config["permission_add"]
#     if not user_has_permission(request.user, permission_name):
#         return HttpResponseForbidden("Permission denied")

#     parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")
#     branch_id = request.GET.get("branch_id") or request.POST.get("branch") or ""
#     area_id = request.GET.get("area_id") or request.POST.get("area") or ""

#     if request.method == "POST":
#         form = form_class(request.POST, request.FILES, instance=instance, request=request)
#         if form.is_valid():
#             obj = form.save()

#             return htmx_trigger_response({
#                 "related:saved": {
#                     "parentField": parent_field,
#                     "option": {
#                         "id": obj.pk,
#                         "text": str(obj)
#                     },
#                     "message": f"{model_name.title()} saved successfully."
#                 }
#             })
#     else:
#         form = form_class(instance=instance, request=request)

#     scope = get_user_scope(request.user)

#     filtered_scope = apply_selected_filters(
#         scope["branches"],
#         scope["areas"],
#         scope["customer_groups"],
#         selected_branch=branch_id or (str(getattr(instance, "branch_id", "") or "")),
#         selected_area=area_id or (str(getattr(instance, "area_id", "") or "")),
#         selected_customer_group_ids=[],
#     )

#     # context = {
#     #     "form": form,
#     #     "model_name": model_name,
#     #     "instance": instance,
#     #     "parent_field": parent_field,
#     #     "branches": filtered_scope["branches"].order_by("name"),
#     #     "areas": filtered_scope["areas"].order_by("name"),
#     #     "customer_groups": filtered_scope["customer_groups"].order_by("name"),
#     #     "selected_branch": branch_id or (str(getattr(instance, "branch_id", "") or "")),
#     #     "selected_area": area_id or (str(getattr(instance, "area_id", "") or "")),
#     # }

#     # return render(request, "common/related_modal_form.html", context)

#     # context = {
#     # "form": form,
#     # "model_name": model_name,
#     # "instance": instance,
#     # "parent_field": parent_field,
#     # "post_url": request.path,
#     # "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
#     # "form_partial_template": "user/model_form.html",
#     # "branches": filtered_scope["branches"].order_by("name"),
#     # "areas": filtered_scope["areas"].order_by("name"),
#     # "customer_groups": filtered_scope["customer_groups"].order_by("name"),
#     # "selected_branch": branch_id or (str(getattr(instance, "branch_id", "") or "")),
#     # "selected_area": area_id or (str(getattr(instance, "area_id", "") or "")),
#     # }

#     # return render(request, "common/related_modal_form.html", context)
#     context = {
#     "form": form,
#     "model_name": model_name,
#     "instance": instance,
#     "parent_field": parent_field,
#     "post_url": request.path,
#     "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
#     "form_partial_template": "user/model_form.html",
# }
#     return render(request, "common/related_modal_form.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def related_object_modal(request, model_name, pk=None):
    model_name = normalize_model_name(model_name)

    MODEL_CONFIG = {
        "branch": {
            "model": Branch,
            "form": BranchQuickForm,
            "permission_add": "user.add_branch",
            "permission_change": "user.change_branch",
        },
        "area": {
            "model": Area,
            "form": AreaQuickForm,
            "permission_add": "user.add_area",
            "permission_change": "user.change_area",
        },
        "customergroup": {
            "model": CustomerGroup,
            "form": CustomerGroupQuickForm,
            "permission_add": "user.add_customergroup",
            "permission_change": "user.change_customergroup",
        },
        "multibranch": {
            "model": MultiBranch,
            "form": MultiBranchQuickForm,
            "permission_add": "user.add_multibranch",
            "permission_change": "user.change_multibranch",
        },
        "role": {
            "model": Roles,
            "form": RoleQuickForm,
            "permission_add": "user.add_role",
            "permission_change": "user.change_role",
        },
        "user": {
            "model": Users,
            "form": UserQuickForm,
            "permission_add": "user.add_users",
            "permission_change": "user.change_users",
        },
        "menu": {
            "model": Menu,
            "form": MenuQuickForm,
            "permission_add": "user.add_menu",
            "permission_change": "user.change_menu",
        },
    }

    if model_name not in MODEL_CONFIG:
        return HttpResponse("Invalid model.", status=400)

    config = MODEL_CONFIG[model_name]
    model_class = config["model"]
    form_class = config["form"]

    instance = get_object_or_404(model_class, pk=pk) if pk else None

    permission_name = config["permission_change"] if instance else config["permission_add"]
    if not user_has_permission(request.user, permission_name):
        return HttpResponseForbidden("Permission denied")

    parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")
    branch_id = request.GET.get("branch_id") or request.POST.get("branch") or ""
    area_id = request.GET.get("area_id") or request.POST.get("area") or ""

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance, request=request)

        if form.is_valid():
            changes = build_form_changes(form) if instance else {}
            obj = form.save()

            action_text = "Updated" if instance else "Created"
            action = "update" if instance else "create"
            target_user = obj if isinstance(obj, Users) else None

            log_activity(
                request,
                action,
                f"{action_text} {obj}",
                target_user=target_user,
                obj=obj,
                changes=changes,
            )

            return htmx_trigger_response({
                "related:saved": {
                    "parentField": parent_field,
                    "option": {
                        "id": obj.pk,
                        "text": str(obj),
                    },
                    "message": f"{action_text} successfully.",
                }
            })

    else:
        form = form_class(instance=instance, request=request)

    context = {
        "form": form,
        "model_name": model_name,
        "instance": instance,
        "parent_field": parent_field,
        "post_url": request.path or "",  # Ensure it's a string, not None
        "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
        "form_partial_template": "user/model_form.html",
        "selected_branch": branch_id or (str(getattr(instance, "branch_id", "") or "")),
        "selected_area": area_id or (str(getattr(instance, "area_id", "") or "")),
    }

    return render(request, "common/universal_modal_form.html", context)



# -------------------------------------------------
# MENU AJAX COMPAT
# -------------------------------------------------

@login_required
@require_http_methods(["POST"])
def menu_ajax_create(request):
    if not user_has_permission(request.user, "user.add_menu"):
        return JsonResponse({"success": False, "message": "Permission denied."}, status=403)

    form = MenuQuickForm(request.POST, request=request)
    if form.is_valid():
        menu = form.save()
        log_activity(request, "create", f"Created menu {menu.name}", obj=menu)
        return JsonResponse(
            {
                "success": True,
                "id": menu.id,
                "text": menu.name,
                "message": "Menu created successfully.",
            }
        )

    return JsonResponse({"success": False, "errors": form.errors}, status=422)


@login_required
@require_GET
def menu_json_detail(request, pk):
    menu = get_object_or_404(Menu.objects.prefetch_related("permissions"), pk=pk)
    return JsonResponse(
        {
            "id": menu.id,
            "name": menu.name,
            "icon": menu.icon,
            "url": menu.url,
            "order": menu.order,
            "is_active": menu.is_active,
            "description": menu.description or "",
            "parent_id": menu.parent_id,
            "permission_ids": list(menu.permissions.values_list("id", flat=True)),
        }
    )


@login_required
@require_http_methods(["POST"])
def menu_ajax_update(request, pk):
    if not user_has_permission(request.user, "user.change_menu"):
        return JsonResponse({"success": False, "message": "Permission denied."}, status=403)

    menu = get_object_or_404(Menu, pk=pk)
    form = MenuQuickForm(request.POST, instance=menu, request=request)

    if form.is_valid():
        changes = build_form_changes(form)
        menu = form.save()
        log_activity(
            request,
            "update",
            f"Updated menu {menu.name}",
            obj=menu,
            changes=changes,
        )
        return JsonResponse(
            {
                "success": True,
                "id": menu.id,
                "text": menu.name,
                "message": "Menu updated successfully.",
            }
        )

    return JsonResponse({"success": False, "errors": form.errors}, status=422)






