from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'department', 'semester', 'email')
    search_fields = ('roll_number', 'full_name', 'email')
    list_filter = ('department', 'semester', 'gender')