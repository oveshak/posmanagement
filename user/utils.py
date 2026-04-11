from .models import ActivityLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_activity(request, action, description, target_user=None):
    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        target_user=target_user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
    )