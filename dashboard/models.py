from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
#
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10, unique=True)
    class_batch = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.full_name

# class Student(models.Model):
#     """
#     Model for storing student information
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     roll_number = models.CharField(max_length=20, unique=True)
#     class_batch = models.CharField(max_length=50, verbose_name="Class/Batch")
#     date_of_birth = models.DateField()
#     is_verified = models.BooleanField(default=False)
#     otp = models.CharField(max_length=6, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.full_name

class Subject(models.Model):
    """
    Model for storing subjects
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    """
    Model for different exam types
    """
    EXAM_TYPES = [
        ('quarterly', 'Quarterly'),
        ('midterm', 'Midterm'),
        ('model', 'Model'),
        ('end_term', 'End-Term'),
    ]
    
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, unique=True)
    name = models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self):
        return self.name

class ProgressSheet(models.Model):
    """
    Model for storing student progress/marks for each exam
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'exam', 'subject')
    
    def __str__(self):
        return f"{self.student.full_name} - {self.exam.name} - {self.subject.name}: {self.marks}"
