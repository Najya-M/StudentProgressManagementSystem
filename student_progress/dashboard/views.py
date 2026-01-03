from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Student, Subject, Exam, ProgressSheet
from .forms import StudentRegistrationForm, StudentProfileForm, LoginForm, OTPVerificationForm, ProgressSheetForm, ExamForm, SubjectForm
import random
import string


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(email, otp):
    """Send OTP to user's email"""
    try:
        send_mail(
            'Email Verification OTP',
            f'Your OTP for email verification is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate and save OTP
            otp = generate_otp()
            student = user.student
            student.otp = otp
            student.save()
            
            # Send OTP to email
            if send_otp_email(student.email, otp):
                messages.success(request, 'Registration successful! Please check your email for OTP verification.')
                return redirect('verify_otp', user_id=user.id)
            else:
                messages.error(request, 'Registration failed. Could not send OTP to your email.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def verify_otp_view(request, user_id):
    """Handle OTP verification"""
    user = get_object_or_404(User, id=user_id)
    student = user.student
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if student.otp == entered_otp:
                student.is_verified = True
                student.otp = None  # Clear OTP after verification
                student.save()
                messages.success(request, 'Email verified successfully! You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'registration/verify_otp.html', {'form': form, 'user_id': user_id})


def resend_otp_view(request, user_id):
    """Resend OTP to user's email"""
    user = get_object_or_404(User, id=user_id)
    student = user.student
    
    # Generate and save new OTP
    otp = generate_otp()
    student.otp = otp
    student.save()
    
    # Send OTP to email
    if send_otp_email(student.email, otp):
        messages.success(request, 'New OTP sent to your email. Please check your inbox.')
    else:
        messages.error(request, 'Failed to send OTP. Please try again later.')
    
    return redirect('verify_otp', user_id=user.id)


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user's email is verified
                try:
                    student = user.student
                    if not student.is_verified:
                        messages.error(request, 'Please verify your email before logging in.')
                        return render(request, 'registration/login.html', {'form': form})
                except Student.DoesNotExist:
                    # If user doesn't have a student profile, they're not a student
                    pass
                
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Main dashboard view"""
    # Get statistics for the dashboard
    total_students = Student.objects.count()
    total_exams = Exam.objects.count()
    total_subjects = Subject.objects.count()
    
    # Get recent activities (last 5 progress entries)
    recent_progress = ProgressSheet.objects.select_related('student', 'exam', 'subject').order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_exams': total_exams,
        'total_subjects': total_subjects,
        'recent_progress': recent_progress,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def student_list_view(request):
    """View to list all students with search and filter capabilities"""
    students = Student.objects.all().order_by('full_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) | 
            Q(roll_number__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort_by', 'full_name')
    if sort_by in ['full_name', 'roll_number', 'class_batch', 'date_of_birth']:
        students = students.order_by(sort_by)
    
    context = {
        'students': students,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/student_list.html', context)


@login_required
def add_student_view(request):
    """View to add a new student"""
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentProfileForm()
    
    return render(request, 'dashboard/add_student.html', {'form': form})


@login_required
def edit_student_view(request, student_id):
    """View to edit student details"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_list')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'dashboard/edit_student.html', {'form': form, 'student': student})


@login_required
def delete_student_view(request, student_id):
    """View to delete a student"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'dashboard/delete_student.html', {'student': student})


@login_required
def progress_sheet_view(request):
    """View to manage student progress sheets"""
    # Get all progress sheets with related data
    progress_sheets = ProgressSheet.objects.select_related('student', 'exam', 'subject').all()
    
    # Filter by exam type if specified
    exam_type = request.GET.get('exam_type', '')
    if exam_type:
        progress_sheets = progress_sheets.filter(exam__exam_type=exam_type)
    
    # Sorting by exam type
    sort_by = request.GET.get('sort_by', 'student__full_name')
    if sort_by in ['student__full_name', 'marks', 'exam__date']:
        progress_sheets = progress_sheets.order_by(sort_by)
    
    # Get all exams for filter dropdown
    exams = Exam.objects.all()
    
    context = {
        'progress_sheets': progress_sheets,
        'exams': exams,
        'selected_exam_type': exam_type,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/progress_sheet.html', context)


@login_required
def add_progress_sheet_view(request):
    """View to add new progress sheet entry"""
    if request.method == 'POST':
        form = ProgressSheetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress sheet entry added successfully!')
            return redirect('progress_sheet')
    else:
        form = ProgressSheetForm()
    
    return render(request, 'dashboard/add_progress_sheet.html', {'form': form})


@login_required
def ranking_view(request):
    """View to display student rankings based on exam performance"""
    exam_type = request.GET.get('exam_type', 'quarterly')
    
    # Get all students who have progress sheets for the selected exam type
    students_with_scores = []
    
    # Get all unique students who have scores for the selected exam type
    students = Student.objects.filter(progresssheet__exam__exam_type=exam_type).distinct()
    
    for student in students:
        # Calculate average score for the selected exam type
        scores = ProgressSheet.objects.filter(
            student=student,
            exam__exam_type=exam_type
        ).values_list('marks', flat=True)
        
        if scores:
            avg_score = sum(scores) / len(scores)
            total_marks = sum(scores)
            students_with_scores.append({
                'student': student,
                'avg_score': avg_score,
                'total_marks': total_marks,
                'num_subjects': len(scores)
            })
    
    # Sort by average score (descending)
    students_with_scores.sort(key=lambda x: x['avg_score'], reverse=True)
    
    # Get all exam types for filter
    exam_types = Exam.objects.values_list('exam_type', flat=True).distinct()
    
    context = {
        'students_with_scores': students_with_scores,
        'selected_exam_type': exam_type,
        'exam_types': exam_types,
    }
    return render(request, 'dashboard/ranking.html', context)


@login_required
def add_exam_view(request):
    """View to add a new exam"""
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully!')
            return redirect('progress_sheet')
    else:
        form = ExamForm()
    
    return render(request, 'dashboard/add_exam.html', {'form': form})


@login_required
def add_subject_view(request):
    """View to add a new subject"""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('progress_sheet')
    else:
        form = SubjectForm()
    
    return render(request, 'dashboard/add_subject.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Create your views here.
