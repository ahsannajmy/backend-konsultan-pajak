from .models import Notifications,AdminNotifications

def notification(request):

    if request.user.is_authenticated:
        if request.user.role == "Admin":
            number_of_admin_notifications = AdminNotifications.objects.filter(user=request.user.id)

            return {
                'number_of_admin_notifications' : len(number_of_admin_notifications)
            }

    number_of_notifications = Notifications.objects.filter(user=request.user.id,is_read=False)

    return {
        'number_of_notifications' : len(number_of_notifications)
    }

def user_information(request):

    if request.user.is_authenticated:
        user = request.user
        return {
            'nama' : user.nama,
            'role' : user.role
        }
    
    return {}