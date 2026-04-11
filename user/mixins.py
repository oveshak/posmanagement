from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin and not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("dashboard")

        return super().dispatch(request, *args, **kwargs)