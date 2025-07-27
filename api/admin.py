from django.contrib import admin
from .models import Programs, Clearance, Signature, Student, ClearanceSignature

admin.site.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'is_staff', 'is_superuser')  # Add other fields you want to show

admin.site.register(Programs)
admin.site.register(Clearance)
admin.site.register(Signature)
admin.site.register(ClearanceSignature)
