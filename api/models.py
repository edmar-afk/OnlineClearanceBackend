from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    year_level = models.CharField(max_length=50)
    major = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - ({self.year_level})"

class Programs(models.Model):
    program_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.program_name

class Clearance(models.Model):
    programs = models.ManyToManyField(Programs, related_name='clearances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    semester = models.CharField(max_length=50, blank=True, null=True)   
    academic_year = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.academic_year}"

class StudentClearance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    clearance = models.ForeignKey(Clearance, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending')
    
    
class Signature(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signatures')
    image = models.FileField(
        upload_to='signatures/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],
        null=True,
        blank=True
    )
    description = models.TextField()
    
class ClearanceSignature(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clearance_signature')
    clearance = models.ForeignKey(StudentClearance, on_delete=models.CASCADE)
    programs = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='clearance_signature')
    receipt = models.FileField(
        upload_to='receipts/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],
        null=True,
        blank=True
    )
    signature = models.ForeignKey(
        Signature,
        on_delete=models.CASCADE,
        related_name='clearance_signature',
        null=True,  
        blank=True
    )
    status = models.CharField(max_length=50, default='Pending')
    feedback = models.TextField(blank=True, null=True)
    
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.user.username}"