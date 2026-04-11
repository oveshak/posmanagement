
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# from .models import Branch, Area, CustomerGroup, Users
# from .forms import BranchForm, AreaForm, CustomerGroupForm, UserForm
# from django.contrib.auth.views import PasswordChangeView



# from .mixins import AdminRequiredMixin
# from .models import ActivityLog, Area, Branch, CustomerGroup, Menu, MultiBranch, Roles, Users
# from .utils import log_activity

# from datetime import datetime, timedelta
# from django.contrib import messages
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import LoginView as DjangoLoginView
# from django.db.models import Prefetch, Q
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.template.loader import render_to_string
# from django.urls import reverse, reverse_lazy
# from django.views.decorators.http import require_GET, require_http_methods
# from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
# from django.utils import timezone

# from .forms import (
  
  
#     CustomPasswordChangeForm,
   
#     CustomAuthenticationForm,
    
  
   
#     UserForm

# )
# from .mixins import AdminRequiredMixin
# from .models import ActivityLog, Area, Branch, CustomerGroup, Menu, MultiBranch, Roles, Users
# from .utils import log_activity


# class CustomLoginView(DjangoLoginView):
#     template_name = "auth/login.html"
#     form_class = CustomAuthenticationForm
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         user = form.get_user()
#         current_time = timezone.now()
#         self.request.session["login_time"] = current_time.isoformat()
#         log_activity(self.request, "login", f"{user} logged in at {current_time.strftime('%I:%M %p')}", user)
#         messages.success(self.request, f"Welcome back, {user.name or user.email}!")
#         return response

#     def form_invalid(self, form):
#         messages.error(self.request, "Invalid email or password. Please try again.")
#         return super().form_invalid(form)

#     def get_success_url(self):
#         return reverse_lazy("dashboard")


# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard/dashboard.html"
#     login_url = "login"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["total_users"] = Users.objects.filter(is_deleted=False).count()
#         context["total_roles"] = Roles.objects.count()
#         context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:10]
#         context["current_user"] = self.request.user
#         return context


# class ManagementDashboardView(AdminRequiredMixin, TemplateView):
#     template_name = "user/management_dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["total_users"] = Users.objects.filter(is_deleted=False).count()
#         context["total_roles"] = Roles.objects.count()
#         context["active_sessions"] = Users.objects.filter(status=True, is_deleted=False).count()
#         context["total_logs"] = ActivityLog.objects.count()
#         context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:5]
#         context["recent_logs_time"] = ActivityLog.objects.latest("created_at").created_at.strftime("%I:%M %p") if ActivityLog.objects.exists() else "N/A"
#         return context


# class AdminDashboardView(AdminRequiredMixin, TemplateView):
#     template_name = "dashboard/admin_dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["total_users"] = Users.objects.filter(is_deleted=False).count()
#         context["total_roles"] = Roles.objects.count()
#         context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:10]
#         return context


# class LogoutView(LoginRequiredMixin, TemplateView):
#     login_url = "login"

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             user_name = request.user.name or request.user.email
#             login_time = request.session.get("login_time")
#             session_duration = "Unknown"
#             if login_time:
#                 try:
#                     login_dt = datetime.fromisoformat(login_time)
#                     duration = timezone.now() - login_dt
#                     minutes = int(duration.total_seconds() // 60)
#                     seconds = int(duration.total_seconds() % 60)
#                     session_duration = f"{minutes}m {seconds}s"
#                 except Exception:
#                     session_duration = "N/A"

#             log_activity(request, "logout", f"{request.user} logged out. Session duration: {session_duration}", request.user)
#             logout(request)
#             messages.success(request, f"Goodbye {user_name}! Session duration: {session_duration}")
#         else:
#             logout(request)
#         return redirect("login")







# class HtmxTemplateView(LoginRequiredMixin, TemplateView):
#     htmx_template_name = None
#     normal_template_name = None
#     login_url = "login"

#     def get_template_names(self):
#         if self.request.headers.get("HX-Request"):
#             return [self.htmx_template_name]
#         return [self.normal_template_name]


# class ProfilePageView(HtmxTemplateView):
#     htmx_template_name = "user/userprofile/user_profile_main.html"
#     normal_template_name = "user/userprofile/user_profile.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["profile_user"] = (
#             Users.objects
#             .select_related("branch", "area")
#             .prefetch_related("roles", "mult_branch", "customer_group")
#             .get(pk=self.request.user.pk)
#         )
#         return context


# class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
#     form_class = CustomPasswordChangeForm
#     template_name = "user/userprofilepassword/change_password.html"
#     success_url = reverse_lazy("profile_page")
#     login_url = "login"

#     def get_template_names(self):
#         if self.request.headers.get("HX-Request"):
#             return ["user/userprofilepassword/change_password_main.html"]
#         return [self.template_name]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["profile_user"] = (
#             Users.objects
#             .select_related("branch", "area")
#             .prefetch_related("roles", "mult_branch", "customer_group")
#             .get(pk=self.request.user.pk)
#         )
#         return context

#     def form_valid(self, form):
#         response = super().form_valid(form)

#         if self.request.headers.get("HX-Request"):
#             messages.success(self.request, "Password changed successfully.")
#             return render(
#                 self.request,
#                 "user/userprofilepassword/password_change_success.html",
#                 {"message": "Password changed successfully."},
#             )

#         return response
# # -------------------------
# # AJAX FILTER
# # -------------------------

# def load_areas(request):
#     branch_id = request.GET.get("branch_id")
#     areas = Area.objects.filter(parent_branch_id=branch_id).values("id", "name")
#     return JsonResponse(list(areas), safe=False)


# def load_customer_groups(request):
#     area_id = request.GET.get("area_id")
#     customer_groups = CustomerGroup.objects.filter(area_id=area_id).values("id", "name")
#     return JsonResponse(list(customer_groups), safe=False)


# # -------------------------
# # BRANCH CRUD
# # -------------------------

# class BranchListView(LoginRequiredMixin, ListView):
#     model = Branch
#     template_name = "branch/list.html"
#     context_object_name = "branches"


# class BranchCreateView(LoginRequiredMixin, CreateView):
#     model = Branch
#     form_class = BranchForm
#     template_name = "branch/form.html"
#     success_url = reverse_lazy("branch_list")

#     def form_valid(self, form):
#         messages.success(self.request, "Branch created successfully.")
#         return super().form_valid(form)


# class BranchUpdateView(LoginRequiredMixin, UpdateView):
#     model = Branch
#     form_class = BranchForm
#     template_name = "branch/form.html"
#     success_url = reverse_lazy("branch_list")

#     def form_valid(self, form):
#         messages.success(self.request, "Branch updated successfully.")
#         return super().form_valid(form)


# class BranchDeleteView(LoginRequiredMixin, DeleteView):
#     model = Branch
#     template_name = "common/confirm_delete.html"
#     success_url = reverse_lazy("branch_list")


# # -------------------------
# # AREA CRUD
# # -------------------------

# class AreaListView(LoginRequiredMixin, ListView):
#     model = Area
#     template_name = "area/list.html"
#     context_object_name = "areas"


# class AreaCreateView(LoginRequiredMixin, CreateView):
#     model = Area
#     form_class = AreaForm
#     template_name = "area/form.html"
#     success_url = reverse_lazy("area_list")

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["branch_id"] = self.request.GET.get("branch")
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, "Area created successfully.")
#         return super().form_valid(form)


# class AreaUpdateView(LoginRequiredMixin, UpdateView):
#     model = Area
#     form_class = AreaForm
#     template_name = "area/form.html"
#     success_url = reverse_lazy("area_list")

#     def form_valid(self, form):
#         messages.success(self.request, "Area updated successfully.")
#         return super().form_valid(form)


# class AreaDeleteView(LoginRequiredMixin, DeleteView):
#     model = Area
#     template_name = "common/confirm_delete.html"
#     success_url = reverse_lazy("area_list")


# # -------------------------
# # CUSTOMER GROUP CRUD
# # -------------------------

# class CustomerGroupListView(LoginRequiredMixin, ListView):
#     model = CustomerGroup
#     template_name = "customer_group/list.html"
#     context_object_name = "customer_groups"


# class CustomerGroupCreateView(LoginRequiredMixin, CreateView):
#     model = CustomerGroup
#     form_class = CustomerGroupForm
#     template_name = "customer_group/form.html"
#     success_url = reverse_lazy("customer_group_list")

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["branch_id"] = self.request.GET.get("branch")
#         kwargs["area_id"] = self.request.GET.get("area")
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, "Customer group created successfully.")
#         return super().form_valid(form)


# class CustomerGroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = CustomerGroup
#     form_class = CustomerGroupForm
#     template_name = "customer_group/form.html"
#     success_url = reverse_lazy("customer_group_list")

#     def form_valid(self, form):
#         messages.success(self.request, "Customer group updated successfully.")
#         return super().form_valid(form)


# class CustomerGroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = CustomerGroup
#     template_name = "common/confirm_delete.html"
#     success_url = reverse_lazy("customer_group_list")


# # -------------------------
# # USER CRUD
# # -------------------------

# class UserListView(LoginRequiredMixin, ListView):
#     model = Users
#     template_name = "users/list.html"
#     context_object_name = "users"


# class UserCreateView(LoginRequiredMixin, CreateView):
#     model = Users
#     form_class = UserForm
#     template_name = "user/form.html"
#     success_url = reverse_lazy("user_list")

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         self.object.sync_staff_relations()
#         messages.success(self.request, "User created successfully.")
#         return response


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = Users
#     form_class = UserForm
#     template_name = "users/form.html"
#     success_url = reverse_lazy("user_list")

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         self.object.sync_staff_relations()
#         messages.success(self.request, "User updated successfully.")
#         return response


# class UserDeleteView(LoginRequiredMixin, DeleteView):
#     model = Users
#     template_name = "common/confirm_delete.html"
#     success_url = reverse_lazy("user_list")



from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView







from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.utils import timezone

from .forms import (
    AreaQuickForm,
    BranchQuickForm,
    CustomPasswordChangeForm,
    CustomerGroupQuickForm,
    CustomAuthenticationForm,
    MenuQuickForm,
    MultiBranchQuickForm,
    RoleForm,
    RoleQuickForm,
    UserCreateForm,
    UserQuickForm,
    UserUpdateForm,
    UserCreateForm,
    UserUpdateForm,
    BranchQuickForm,
    AreaQuickForm,
    CustomerGroupQuickForm,
    MenuQuickForm,
    UserQuickForm,
    RoleQuickForm,
    UserForm

)
from .mixins import AdminRequiredMixin
from .models import ActivityLog, Area, Branch, CustomerGroup, Menu, MultiBranch, Roles, Users
from .utils import log_activity


class CustomLoginView(DjangoLoginView):
    template_name = "auth/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        current_time = timezone.now()
        self.request.session["login_time"] = current_time.isoformat()
        log_activity(self.request, "login", f"{user} logged in at {current_time.strftime('%I:%M %p')}", user)
        messages.success(self.request, f"Welcome back, {user.name or user.email}!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.filter(is_deleted=False).count()
        context["total_roles"] = Roles.objects.count()
        context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:10]
        context["current_user"] = self.request.user
        return context


class ManagementDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "user/management_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.filter(is_deleted=False).count()
        context["total_roles"] = Roles.objects.count()
        context["active_sessions"] = Users.objects.filter(status=True, is_deleted=False).count()
        context["total_logs"] = ActivityLog.objects.count()
        context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:5]
        context["recent_logs_time"] = ActivityLog.objects.latest("created_at").created_at.strftime("%I:%M %p") if ActivityLog.objects.exists() else "N/A"
        return context


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Users.objects.filter(is_deleted=False).count()
        context["total_roles"] = Roles.objects.count()
        context["recent_logs"] = ActivityLog.objects.select_related("user", "target_user")[:10]
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    login_url = "login"

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

            log_activity(request, "logout", f"{request.user} logged out. Session duration: {session_duration}", request.user)
            logout(request)
            messages.success(request, f"Goodbye {user_name}! Session duration: {session_duration}")
        else:
            logout(request)
        return redirect("login")







class HtmxTemplateView(LoginRequiredMixin, TemplateView):
    htmx_template_name = None
    normal_template_name = None
    login_url = "login"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return [self.htmx_template_name]
        return [self.normal_template_name]


class ProfilePageView(HtmxTemplateView):
    htmx_template_name = "user/userprofile/user_profile_main.html"
    normal_template_name = "user/userprofile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = (
            Users.objects
            .select_related("branch", "area")
            .prefetch_related("roles", "mult_branch", "customer_group")
            .get(pk=self.request.user.pk)
        )
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "user/userprofilepassword/change_password.html"
    success_url = reverse_lazy("profile_page")
    login_url = "login"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["user/userprofilepassword/change_password_main.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = (
            Users.objects
            .select_related("branch", "area")
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




# class ProfilePageView(LoginRequiredMixin, TemplateView):
#     template_name = "user/user_profile.html"
#     login_url = "login"



# from .forms import CustomPasswordChangeForm 
# from django.contrib.auth.views import PasswordChangeView

# class HtmxTemplateView(LoginRequiredMixin, TemplateView):
#     htmx_template_name = None
#     normal_template_name = None
#     login_url = "login"

#     def get_template_names(self):
#         if self.request.headers.get("HX-Request"):
#             return [self.htmx_template_name]
#         return [self.normal_template_name]


# class ProfilePageView(HtmxTemplateView):
#     htmx_template_name = "user/userprofile/user_profile_main.html"
#     normal_template_name = "user/userprofile/user_profile.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["profile_user"] = (
#             Users.objects
#             .select_related("branch", "area")
#             .prefetch_related("roles", "mult_branch", "customer_group")
#             .get(pk=self.request.user.pk)
#         )
#         return context


# class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
#     form_class = CustomPasswordChangeForm
#     template_name = "user/userprofilepassword/change_password.html"
#     success_url = reverse_lazy("profile_page")
#     login_url = "login"

#     def get_template_names(self):
#         if self.request.headers.get("HX-Request"):
#             return ["user/userprofilepassword/change_password_main.html"]
#         return [self.template_name]

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, "Password changed successfully.")

#         if self.request.headers.get("HX-Request"):
#             return render(
#                 self.request,
#                 "user/userprofilepassword/password_change_success.html",
#                 {"message": "Password changed successfully."},
#             )
#         return response







from django.db.models import Q
from django.views.generic import ListView

class UserListView( ListView):
    model = Users
    template_name = "user/user_list.html"
    context_object_name = "users"
    paginate_by = 10

    def is_global_user(self):
        # শুধু superuser সব দেখতে পারবে
        return self.request.user.is_superuser

    def get_allowed_branch_ids(self):
        user = self.request.user

        if self.is_global_user():
            return None

        if user.branch_id:
            return [user.branch_id]

        multi_branch_sets = user.mult_branch.all()
        if multi_branch_sets.exists():
            return list(
                Branch.objects.filter(
                    multibranch__in=multi_branch_sets
                ).values_list("id", flat=True).distinct()
            )

        return []

    def get_allowed_area_ids(self):
        user = self.request.user

        if self.is_global_user():
            return None

        if user.area_id:
            return [user.area_id]

        branch_ids = self.get_allowed_branch_ids()
        if branch_ids:
            return list(
                Area.objects.filter(parent_branch_id__in=branch_ids)
                .values_list("id", flat=True)
                .distinct()
            )

        return []

    def get_allowed_customer_group_ids(self):
        user = self.request.user

        if self.is_global_user():
            return None

        # user-er nijer assigned customer groups থাকলে শুধু ওইগুলো
        user_group_ids = list(user.customer_group.values_list("id", flat=True))
        if user_group_ids:
            return user_group_ids

        # না থাকলে area/branch অনুযায়ী possible groups
        area_ids = self.get_allowed_area_ids()
        branch_ids = self.get_allowed_branch_ids()

        qs = CustomerGroup.objects.all()

        if area_ids:
            qs = qs.filter(area_id__in=area_ids)
        elif branch_ids:
            qs = qs.filter(branch_id__in=branch_ids)
        else:
            qs = qs.none()

        return list(qs.values_list("id", flat=True).distinct())

    def get_queryset(self):
        queryset = (
            Users.objects.filter(is_deleted=False)
            .prefetch_related("roles", "mult_branch", "customer_group")
            .select_related("branch", "area")
        )

        search = self.request.GET.get("search")
        branch_id = self.request.GET.get("branch")
        area_id = self.request.GET.get("area")
        customer_group_id = self.request.GET.get("customer_group")
        role_id = self.request.GET.get("role")
        created_from = self.request.GET.get("created_from")
        created_to = self.request.GET.get("created_to")

        user = self.request.user

        # SUPERUSER ছাড়া সবাই restricted
        if not self.is_global_user():
            # base restriction: exact hierarchy
            if user.area_id:
                queryset = queryset.filter(area_id=user.area_id)
            elif user.branch_id:
                queryset = queryset.filter(branch_id=user.branch_id)
            else:
                branch_ids = self.get_allowed_branch_ids()
                if branch_ids:
                    queryset = queryset.filter(branch_id__in=branch_ids)
                else:
                    queryset = queryset.none()

            # customer group restriction: যদি login user-er customer group assign থাকে
            user_group_ids = list(user.customer_group.values_list("id", flat=True))
            if user_group_ids:
                queryset = queryset.filter(customer_group__id__in=user_group_ids)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )

        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)

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

        selected_branch = self.request.GET.get("branch")
        selected_area = self.request.GET.get("area")
        user = self.request.user

        if self.is_global_user():
            branches = Branch.objects.order_by("name")
            areas = Area.objects.order_by("name")
            customer_groups = CustomerGroup.objects.order_by("name")
        else:
            allowed_branch_ids = self.get_allowed_branch_ids()
            allowed_area_ids = self.get_allowed_area_ids()

            branches = Branch.objects.none()
            areas = Area.objects.none()
            customer_groups = CustomerGroup.objects.none()

            if allowed_branch_ids:
                branches = Branch.objects.filter(id__in=allowed_branch_ids).order_by("name")

            if allowed_area_ids:
                areas = Area.objects.filter(id__in=allowed_area_ids).order_by("name")

            # customer group dropdown
            user_group_ids = list(user.customer_group.values_list("id", flat=True))
            if user_group_ids:
                customer_groups = CustomerGroup.objects.filter(id__in=user_group_ids).order_by("name")
            elif user.area_id:
                customer_groups = CustomerGroup.objects.filter(area_id=user.area_id).order_by("name")
            elif allowed_branch_ids:
                customer_groups = CustomerGroup.objects.filter(branch_id__in=allowed_branch_ids).order_by("name")

        if selected_branch:
            areas = areas.filter(parent_branch_id=selected_branch)

        if selected_area:
            customer_groups = customer_groups.filter(area_id=selected_area)
        elif selected_branch:
            customer_groups = customer_groups.filter(branch_id=selected_branch)

        context["branches"] = branches.distinct()
        context["areas"] = areas.distinct()
        context["customer_groups"] = customer_groups.distinct()
        context["roles"] = Roles.objects.order_by("name")
        return context



# class UserFormContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["branch_quick_form"] = BranchQuickForm()
#         context["area_quick_form"] = AreaQuickForm()
#         context["multibranch_quick_form"] = MultiBranchQuickForm()
#         context["role_quick_form"] = RoleQuickForm()
#         context["customergroup_quick_form"] = CustomerGroupQuickForm()
#         return context



# class UserFormContextMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["branch_quick_form"] = BranchQuickForm()
#         context["area_quick_form"] = AreaQuickForm()
#         context["multibranch_quick_form"] = MultiBranchQuickForm()
#         context["role_quick_form"] = RoleQuickForm()
#         context["customergroup_quick_form"] = CustomerGroupQuickForm()
#         context["user_quick_form"] = UserQuickForm()
#         return context

# class UserCreateView( UserFormContextMixin, CreateView):
#     model = Users
#     form_class = UserCreateForm
#     template_name = "user/user_form.html"
#     success_url = reverse_lazy("user_list")

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["request"] = self.request
#         return kwargs

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         log_activity(self.request, "create", f"Created user {self.object.email}", self.object)
#         messages.success(self.request, "User created successfully.")
#         return response


# class UserUpdateView( UserFormContextMixin, UpdateView):
#     model = Users
#     form_class = UserUpdateForm
#     template_name = "user/user_form.html"
#     success_url = reverse_lazy("user_list")

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["request"] = self.request
#         return kwargs

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         log_activity(self.request, "update", f"Updated user {self.object.email}", self.object)
#         messages.success(self.request, "User updated successfully.")
#         return response

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db import transaction

from .models import Users, Roles, Branch, Area, MultiBranch, CustomerGroup
from .utils import log_activity


class UserFormContextMixin:
    template_name = "user/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_common_context(self, request, obj=None, errors=None):
        selected_branch = request.POST.get("branch") or (obj.branch_id if obj and obj.branch_id else "")
        selected_area = request.POST.get("area") or (obj.area_id if obj and obj.area_id else "")

        branches = Branch.objects.order_by("name")
        areas = Area.objects.order_by("name")
        customer_groups = CustomerGroup.objects.order_by("name")
        roles = Roles.objects.order_by("name")
        multibranches = MultiBranch.objects.order_by("title")

        if selected_branch:
            areas = areas.filter(parent_branch_id=selected_branch)
            customer_groups = customer_groups.filter(branch_id=selected_branch)

        if selected_area:
            customer_groups = customer_groups.filter(area_id=selected_area)

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

        return {
            "object": obj,
            "errors": errors or {},
            "branches": branches.distinct(),
            "areas": areas.distinct(),
            "customer_groups": customer_groups.distinct(),
            "roles": roles,
            "multibranches": multibranches,
            "selected_role_ids": selected_role_ids,
            "selected_mult_branch_ids": selected_mult_branch_ids,
            "selected_customer_group_ids": selected_customer_group_ids,
        }

    def _sync_user_staff_links(self, user):
        """
        Keep reverse staff M2M relations in sync with user.branch, user.area,
        and user.customer_group.
        """

        # clear old reverse links first
        for branch in Branch.objects.filter(branchStaff=user):
            branch.branchStaff.remove(user)

        for area in Area.objects.filter(area_staf=user):
            area.area_staf.remove(user)

        for cg in CustomerGroup.objects.filter(customer_group_Staff=user):
            cg.customer_group_Staff.remove(user)

        # infer missing branch/area from selected area / customer groups
        branch_updated = False
        area_updated = False

        if user.area and user.area.parent_branch and not user.branch:
            user.branch = user.area.parent_branch
            branch_updated = True

        for cg in user.customer_group.all():
            if not user.branch and cg.branch:
                user.branch = cg.branch
                branch_updated = True
            if not user.area and cg.area:
                user.area = cg.area
                area_updated = True

        if branch_updated or area_updated:
            update_fields = []
            if branch_updated:
                update_fields.append("branch")
            if area_updated:
                update_fields.append("area")
            user.save(update_fields=update_fields)

        # add to branch staff
        if user.branch:
            user.branch.branchStaff.add(user)

        # add to area staff
        if user.area:
            user.area.area_staf.add(user)

        # add to customer group staff
        for cg in user.customer_group.all():
            cg.customer_group_Staff.add(user)

        # optional consistency update:
        # if user has area but no branch staff relation from area's parent branch
        if user.area and user.area.parent_branch:
            user.area.parent_branch.total_area.add(user.area)

        # if selected customer groups have branch/area and user still missing one
        # this should already be handled above, but safe to keep consistent
        if user.area and user.area.parent_branch and not user.branch:
            user.branch = user.area.parent_branch
            user.save(update_fields=["branch"])


class UserCreateView(LoginRequiredMixin, UserFormContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_common_context(request, obj=None)
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

        log_activity(request, "create", f"Created user {user.email}", user)
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

        log_activity(request, "update", f"Updated user {obj.email}", obj)
        messages.success(request, "User updated successfully.")
        return redirect(self.success_url)

class UserDeleteView( DeleteView):
    model = Users
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        user = self.get_object()
        user.is_deleted = True
        user.save(update_fields=["is_deleted"])
        log_activity(self.request, "delete", f"Soft deleted user {user.email}", user)
        messages.success(self.request, "User deleted successfully.")
        return redirect(self.success_url)


class RoleListView(ListView):
    model = Roles
    template_name = "user/role_list.html"
    context_object_name = "roles"

    def get_queryset(self):
        return Roles.objects.prefetch_related("permissions", "user_roles", "menu").all()


class RoleCreateView(CreateView):
    model = Roles
    form_class = RoleForm
    template_name = "user/role_form.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request, "role_update", f"Created role {self.object.name}")
        messages.success(self.request, "Role created successfully.")
        return response


class RoleUpdateView(UpdateView):
    model = Roles
    form_class = RoleForm
    template_name = "user/role_form.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request, "role_update", f"Updated role {self.object.name}")
        messages.success(self.request, "Role updated successfully.")
        return response


class RoleDeleteView(DeleteView):
    model = Roles
    template_name = "user/role_confirm_delete.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        role = self.get_object()
        log_activity(self.request, "role_update", f"Deleted role {role.name}")
        messages.success(self.request, "Role deleted successfully.")
        return super().form_valid(form)


class CustomerGroupDeleteView(DeleteView):
    model = CustomerGroup
    success_url = reverse_lazy("customer_group_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm('user.delete_customergroup')):
            messages.error(request, "You don't have permission to delete customer groups.")
            return redirect('customer_group_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cg = self.get_object()
        # Clear customer group staff relationships
        cg.customer_group_Staff.clear()
        log_activity(self.request, "customer_group_delete", f"Deleted customer group {cg.name}")
        messages.success(self.request, "Customer group deleted successfully.")
        return super().form_valid(form)


class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy("menu_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm('user.delete_menu')):
            messages.error(request, "You don't have permission to delete menus.")
            return redirect('menu_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        menu = self.get_object()
        # Remove this menu from all roles
        menu.role_menu_items.clear()
        # Update any child menus to have no parent
        Menu.objects.filter(parent=menu).update(parent=None)
        log_activity(self.request, "menu_delete", f"Deleted menu {menu.name}")
        messages.success(self.request, "Menu deleted successfully.")
        return super().form_valid(form)


class BranchDeleteView(DeleteView):
    model = Branch
    success_url = reverse_lazy("branch_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm('user.delete_branch')):
            messages.error(request, "You don't have permission to delete branches.")
            return redirect('branch_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        branch = self.get_object()
        # Clear branch staff relationships
        branch.branchStaff.clear()
        # Clear areas from this branch
        branch.total_area.clear()
        log_activity(self.request, "branch_delete", f"Deleted branch {branch.name}")
        messages.success(self.request, "Branch deleted successfully.")
        return super().form_valid(form)


class AreaDeleteView(DeleteView):
    model = Area
    success_url = reverse_lazy("area_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm('user.delete_area')):
            messages.error(request, "You don't have permission to delete areas.")
            return redirect('area_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        area = self.get_object()
        # Clear area staff relationships
        area.area_staf.clear()
        # Remove this area from all branches that have it in total_area
        area.branches.all().clear()
        log_activity(self.request, "area_delete", f"Deleted area {area.name}")
        messages.success(self.request, "Area deleted successfully.")
        return super().form_valid(form)

class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    template_name = "user/branch_list.html"
    context_object_name = "branches"

    def get_queryset(self):
        return Branch.objects.select_related("manager").prefetch_related("branchStaff", "total_area", "users").all()


class AreaListView(LoginRequiredMixin, ListView):
    model = Area
    template_name = "user/area_list.html"
    context_object_name = "areas"

    def get_queryset(self):
        return Area.objects.select_related("parent_branch").prefetch_related("area_staf", "users_area").all()


class CustomerGroupListView(LoginRequiredMixin, ListView):
    model = CustomerGroup
    template_name = "user/customer_group_list.html"
    context_object_name = "customer_groups"

    def get_queryset(self):
        return CustomerGroup.objects.select_related("branch", "area").prefetch_related("customer_group_Staff").all()


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    template_name = "user/menu_list.html"
    context_object_name = "menus"

    def get_queryset(self):
        return Menu.objects.select_related("parent").prefetch_related("permissions", "role_menu_items").all()

# class ActivityLogListView( ListView):
#     model = ActivityLog
#     template_name = "user/activity_log.html"
#     context_object_name = "logs"
#     paginate_by = 20

#     def get_queryset(self):
#         return ActivityLog.objects.select_related("user", "target_user").order_by("-created_at")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today = timezone.now().date()
#         week_ago = timezone.now() - timedelta(days=7)
#         month_ago = timezone.now() - timedelta(days=30)
#         context["today_count"] = ActivityLog.objects.filter(created_at__date=today).count()
#         context["week_count"] = ActivityLog.objects.filter(created_at__gte=week_ago).count()
#         context["month_count"] = ActivityLog.objects.filter(created_at__gte=month_ago).count()
#         return context




class ActivityLogListView(ListView):
    model = ActivityLog
    template_name = "user/activity_log.html"
    context_object_name = "logs"
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            ActivityLog.objects
            .select_related("user", "target_user", "user__branch", "user__area")
            .prefetch_related("user__customer_group")
            .order_by("-created_at")
        )

        search = self.request.GET.get("search", "").strip()
        user_id = self.request.GET.get("user", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()
        area_id = self.request.GET.get("area", "").strip()
        customer_group_id = self.request.GET.get("customer_group", "").strip()
        action = self.request.GET.get("action", "").strip()
        from_date = self.request.GET.get("from_date", "").strip()
        to_date = self.request.GET.get("to_date", "").strip()

        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(user__name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(target_user__name__icontains=search) |
                Q(target_user__email__icontains=search)
            )

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

        selected_branch = self.request.GET.get("branch", "").strip()
        selected_area = self.request.GET.get("area", "").strip()

        context["users"] = Users.objects.filter(is_deleted=False).order_by("name")
        context["branches"] = Branch.objects.order_by("name")

        if selected_branch:
            context["areas"] = Area.objects.filter(parent_branch_id=selected_branch).order_by("name")
        else:
            context["areas"] = Area.objects.order_by("name")

        customer_groups = CustomerGroup.objects.all()

        if selected_branch:
            customer_groups = customer_groups.filter(branch_id=selected_branch)

        if selected_area:
            customer_groups = customer_groups.filter(area_id=selected_area)

        context["customer_groups"] = customer_groups.order_by("name").distinct()

        context["selected_search"] = self.request.GET.get("search", "")
        context["selected_user"] = self.request.GET.get("user", "")
        context["selected_branch"] = selected_branch
        context["selected_area"] = selected_area
        context["selected_customer_group"] = self.request.GET.get("customer_group", "")
        context["selected_action"] = self.request.GET.get("action", "")
        context["selected_from_date"] = self.request.GET.get("from_date", "")
        context["selected_to_date"] = self.request.GET.get("to_date", "")

        filtered_logs = self.get_queryset()
        now = timezone.now()

        context["today_count"] = filtered_logs.filter(created_at__date=now.date()).count()
        context["week_count"] = filtered_logs.filter(created_at__gte=now - timedelta(days=7)).count()
        context["month_count"] = filtered_logs.filter(created_at__gte=now - timedelta(days=30)).count()

        return context





from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404

from .models import Menu


@login_required
@permission_required("user.add_menu", raise_exception=True)
@require_POST
def menu_ajax_create(request):
    name = request.POST.get("name", "").strip()
    url = request.POST.get("url", "").strip()
    icon = request.POST.get("icon", "").strip() or "fas fa-circle"
    order = request.POST.get("order", "0").strip()
    description = request.POST.get("description", "").strip()
    parent_id = request.POST.get("parent", "").strip()
    is_active = request.POST.get("is_active") == "on"

    if not name:
        return JsonResponse({"success": False, "error": "Menu name is required."})

    if not url:
        return JsonResponse({"success": False, "error": "URL is required."})

    try:
        order = int(order or 0)
    except ValueError:
        return JsonResponse({"success": False, "error": "Order must be a number."})

    parent = None
    if parent_id:
        parent = get_object_or_404(Menu, pk=parent_id)

    menu = Menu.objects.create(
        name=name,
        url=url,
        icon=icon,
        order=order,
        description=description,
        parent=parent,
        is_active=is_active,
    )

    return JsonResponse({
        "success": True,
        "id": menu.id,
        "text": str(menu),
    })


@login_required
@permission_required("user.change_menu", raise_exception=True)
@require_GET
def menu_json_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    return JsonResponse({
        "success": True,
        "id": menu.id,
        "name": menu.name,
        "url": menu.url,
        "icon": menu.icon,
        "order": menu.order,
        "description": menu.description or "",
        "parent": menu.parent_id or "",
        "is_active": menu.is_active,
        "text": str(menu),
    })


@login_required
@permission_required("user.change_menu", raise_exception=True)
@require_POST
def menu_ajax_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    name = request.POST.get("name", "").strip()
    url = request.POST.get("url", "").strip()
    icon = request.POST.get("icon", "").strip() or "fas fa-circle"
    order = request.POST.get("order", "0").strip()
    description = request.POST.get("description", "").strip()
    parent_id = request.POST.get("parent", "").strip()
    is_active = request.POST.get("is_active") == "on"

    if not name:
        return JsonResponse({"success": False, "error": "Menu name is required."})

    if not url:
        return JsonResponse({"success": False, "error": "URL is required."})

    try:
        order = int(order or 0)
    except ValueError:
        return JsonResponse({"success": False, "error": "Order must be a number."})

    parent = None
    if parent_id:
        parent = get_object_or_404(Menu, pk=parent_id)
        if parent.pk == menu.pk:
            return JsonResponse({"success": False, "error": "A menu cannot be its own parent."})

    menu.name = name
    menu.url = url
    menu.icon = icon
    menu.order = order
    menu.description = description
    menu.parent = parent
    menu.is_active = is_active
    menu.save()

    return JsonResponse({
        "success": True,
        "id": menu.id,
        "text": str(menu),
    })



# ---------- AJAX helpers ----------
def object_label(obj):
    if hasattr(obj, "name") and obj.name:
        return f"{obj.pk} - {obj.name}"
    if hasattr(obj, "title") and obj.title:
        return f"{obj.pk} - {obj.title}"
    if hasattr(obj, "email") and obj.email:
        return f"{obj.pk} - {obj.email}"
    return f"{obj.pk} - {obj}"







def serialize_instance(instance, form_class):
    form = form_class(instance=instance)
    data = {}

    for name in form.fields.keys():
        value = getattr(instance, name, None)

        if hasattr(value, "all"):
            data[name] = list(value.all().values_list("pk", flat=True))
        elif hasattr(instance, f"{name}_id"):
            data[name] = getattr(instance, f"{name}_id")
        else:
            data[name] = value if value is not None else ""

    return data


def compact_option(obj):
    if not obj:
        return None
    return {
        "id": obj.pk,
        "text": object_label(obj),
    }


def build_related_save_payload(model_name, obj):
    payload = {
        "success": True,
        "model": model_name,
        "item": compact_option(obj),
        "message": f"{model_name.title()} saved successfully.",
    }

    if model_name == "branch":
        payload["branch"] = compact_option(obj)

    elif model_name == "area":
        payload["branch"] = compact_option(obj.parent_branch) if obj.parent_branch_id else None
        payload["area"] = compact_option(obj)

    elif model_name == "customergroup":
        payload["branch"] = compact_option(obj.branch) if obj.branch_id else None
        payload["area"] = compact_option(obj.area) if obj.area_id else None
        payload["customer_group"] = compact_option(obj)

    elif model_name == "multibranch":
        payload["mult_branch"] = compact_option(obj)

    elif model_name == "role":
        payload["role"] = compact_option(obj)

    elif model_name == "user":
        payload["user"] = compact_option(obj)
        payload["branch"] = compact_option(obj.branch) if getattr(obj, "branch_id", None) else None
        payload["area"] = compact_option(obj.area) if getattr(obj, "area_id", None) else None

    return payload



@login_required
@require_GET
def ajax_areas_by_branch(request):
    branch_id = request.GET.get("branch_id")

    qs = Area.objects.filter(parent_branch_id=branch_id).order_by("name") if branch_id else Area.objects.none()

    return JsonResponse({
        "results": [
            {
                "id": item.id,
                "text": item.name,
                "branch_id": item.parent_branch_id,
            }
            for item in qs
        ]
    })


@login_required
@require_GET
def ajax_customer_groups(request):
    branch_id = request.GET.get("branch_id")
    area_id = request.GET.get("area_id")

    qs = CustomerGroup.objects.all().order_by("name")

    if branch_id:
        qs = qs.filter(branch_id=branch_id)

    if area_id:
        qs = qs.filter(area_id=area_id)

    return JsonResponse({
        "results": [
            {
                "id": item.id,
                "text": item.name,
                "branch_id": item.branch_id,
                "area_id": item.area_id,
            }
            for item in qs
        ]
    })


@login_required
@require_GET
def ajax_branch_meta(request, pk):
    branch = get_object_or_404(
        Branch.objects.prefetch_related("branchStaff", "total_area"),
        pk=pk,
    )
    return JsonResponse({
        "id": branch.id,
        "manager_id": branch.manager_id,
        "staff_ids": list(branch.branchStaff.values_list("id", flat=True)),
        "area_ids": list(branch.total_area.values_list("id", flat=True)),
    })


@login_required
@require_GET
def ajax_area_meta(request, pk):
    area = get_object_or_404(
        Area.objects.prefetch_related("area_staf", "customer_groups"),
        pk=pk,
    )
    return JsonResponse({
        "id": area.id,
        "branch_id": area.parent_branch_id,
        "staff_ids": list(area.area_staf.values_list("id", flat=True)),
        "customer_group_ids": list(area.customer_groups.values_list("id", flat=True)),
    })
    branch_id = request.GET.get("branch_id")
    area_id = request.GET.get("area_id")

    qs = CustomerGroup.objects.all().order_by("name")

    if branch_id:
        qs = qs.filter(branch_id=branch_id)

    if area_id:
        qs = qs.filter(area_id=area_id)

    return JsonResponse({
        "results": [
            {
                "id": item.id,
                "text": item.name,
            }
            for item in qs
        ]
    })

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .models import Users, Roles, Branch, Area, MultiBranch, Menu, CustomerGroup
from .forms import (
    UserForm,
    RoleQuickForm,
    BranchQuickForm,
    AreaQuickForm,
    CustomerGroupQuickForm,
    MenuQuickForm,
)


MODEL_FORM_MAP = {
    "branch": (Branch, BranchQuickForm),
    "area": (Area, AreaQuickForm),
    "customergroup": (CustomerGroup, CustomerGroupQuickForm),
    "multibranch": (MultiBranch, MultiBranchQuickForm),
    "role": (Roles, RoleQuickForm),
    "menu": (Menu, MenuQuickForm),
    "user": (Users, UserForm),
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



def compact_option(obj):
    return {
        "id": obj.pk,
        "text": str(obj),
    }

def build_related_save_payload(model_name, obj):
    payload = {
        "success": True,
        "item": compact_option(obj),
    }

    if model_name == "branch":
        payload["branch"] = compact_option(obj)

    elif model_name == "area":
        payload["area"] = compact_option(obj)
        if getattr(obj, "parent_branch_id", None):
            payload["branch"] = compact_option(obj.parent_branch)

    elif model_name == "customergroup":
        payload["customergroup"] = compact_option(obj)
        payload["customer_group"] = compact_option(obj)
        if getattr(obj, "branch_id", None):
            payload["branch"] = compact_option(obj.branch)
        if getattr(obj, "area_id", None):
            payload["area"] = compact_option(obj.area)

    elif model_name == "multibranch":
        payload["multibranch"] = compact_option(obj)

    elif model_name == "role":
        payload["role"] = compact_option(obj)

    elif model_name == "menu":
        payload["menu"] = compact_option(obj)

    elif model_name == "user":
        payload["user"] = compact_option(obj)

    return payload

@login_required
@require_http_methods(["GET", "POST"])
def related_object_modal(request, model_name, pk=None):
    model_name = model_name.lower().strip()

    if model_name not in MODEL_FORM_MAP:
        return JsonResponse({"success": False, "message": "Invalid model name."}, status=400)

    model_class, form_class = MODEL_FORM_MAP[model_name]
    if form_class is None:
        return JsonResponse({"success": False, "message": "Form is not configured for this model."}, status=400)

    add_perm, change_perm = MODEL_PERMISSION_MAP[model_name]

    if pk:
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm(change_perm)):
            raise PermissionDenied
    else:
        if not (request.user.is_superuser or request.user.is_admin or request.user.has_perm(add_perm)):
            raise PermissionDenied

    instance = get_object_or_404(model_class, pk=pk) if pk else None
    initial = {}

    if request.method == "GET":
        if model_name == "area" and request.GET.get("branch_id"):
            try:
                initial["parent_branch"] = Branch.objects.get(pk=request.GET.get("branch_id"))
            except Branch.DoesNotExist:
                pass

        elif model_name == "customergroup":
            if request.GET.get("branch_id"):
                try:
                    initial["branch"] = Branch.objects.get(pk=request.GET.get("branch_id"))
                except Branch.DoesNotExist:
                    pass

            if request.GET.get("area_id"):
                try:
                    area = Area.objects.get(pk=request.GET.get("area_id"))
                    initial["area"] = area
                    if not initial.get("branch") and getattr(area, "parent_branch", None):
                        initial["branch"] = area.parent_branch
                except Area.DoesNotExist:
                    pass

        elif model_name == "menu" and request.GET.get("parent_id"):
            try:
                initial["parent"] = Menu.objects.get(pk=request.GET.get("parent_id"))
            except Menu.DoesNotExist:
                pass

        form = form_class(instance=instance, initial=initial, request=request)

        html = render_to_string(
            "user/modal_form.html",
            {
                "form": form,
                "instance": instance,
                "model_name": model_name,
                "title": f"{'Edit' if instance else 'Create'} {model_class._meta.verbose_name.title()}",
            },
            request=request,
        )
        return JsonResponse({"success": True, "html": html})

    form = form_class(request.POST, request.FILES, instance=instance, request=request)

    if form.is_valid():
        obj = form.save()
        return JsonResponse(build_related_save_payload(model_name, obj))

    html = render_to_string(
        "user/modal_form.html",
        {
            "form": form,
            "instance": instance,
            "model_name": model_name,
            "title": f"{'Edit' if instance else 'Create'} {model_class._meta.verbose_name.title()}",
        },
        request=request,
    )
    return JsonResponse({"success": False, "html": html, "errors": form.errors}, status=400)


@login_required
def test_widgets(request):
    """Debug view to test widget rendering"""
    form = CustomerGroupQuickForm(request=request)
    return render(request, "user/test_widget.html", {"form": form})














