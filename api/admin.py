from django.contrib import admin
from .models import Programs, Clearance, Signature, Student

admin.site.register(Programs)
admin.site.register(Clearance)
admin.site.register(Signature)
admin.site.register(Student)