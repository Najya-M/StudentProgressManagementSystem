from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Subject, Exam, ProgressSheet


class StudentRegistrationForm(UserCreationForm):
    """
    Form for student registration with additional fields
    """
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    roll_number = forms.CharField(max_length=20, required=True)
    class_batch = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create associated student profile
            student = Student.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                roll_number=self.cleaned_data['roll_number'],
                class_batch=self.cleaned_data['class_batch'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user


class StudentProfileForm(forms.ModelForm):
    """
    Form for updating student profile
    """
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'roll_number', 'class_batch', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    """
    Form for user login
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class OTPVerificationForm(forms.Form):
    """
    Form for OTP verification
    """
    otp = forms.CharField(max_length=6, min_length=6)


class ProgressSheetForm(forms.ModelForm):
    """
    Form for entering progress/marks
    """
    class Meta:
        model = ProgressSheet
        fields = ['student', 'exam', 'subject', 'marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'min': 0, 'max': 100})
        }


class ExamForm(forms.ModelForm):
    """
    Form for creating exams
    """
    class Meta:
        model = Exam
        fields = ['exam_type', 'name', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class SubjectForm(forms.ModelForm):
    """
    Form for creating subjects
    """
    class Meta:
        model = Subject
        fields = ['name']