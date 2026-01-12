
from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        # Changed order_description to order_by
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:5]
        return {
            'notifications': notifications,
            'notif_count': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {'notifications': [], 'notif_count': 0}