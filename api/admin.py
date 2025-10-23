from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Programs, Clearance, Signature, Student, ClearanceSignature, Notification, StudentClearance

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(ClearanceSignature)
class ClearanceSignatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'clearance', 'programs', 'status', 'signature', 'feedback')
    search_fields = ('student__username', 'programs__program_name', 'status')
    list_filter = ('status', 'programs')

admin.site.register(Student)
admin.site.register(Programs)
admin.site.register(Clearance)
admin.site.register(Signature)
admin.site.register(Notification)
