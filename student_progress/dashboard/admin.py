from django.contrib import admin
from .models import Student, Subject, Exam, ProgressSheet

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'roll_number', 'class_batch', 'is_verified', 'created_at']
    list_filter = ['class_batch', 'is_verified', 'created_at']
    search_fields = ['full_name', 'email', 'roll_number']
    ordering = ['full_name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'date']
    list_filter = ['exam_type', 'date']
    ordering = ['-date']

@admin.register(ProgressSheet)
class ProgressSheetAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks', 'created_at']
    list_filter = ['exam', 'subject', 'marks']
    search_fields = ['student__full_name', 'student__roll_number']
    ordering = ['student__full_name', 'exam__date']
