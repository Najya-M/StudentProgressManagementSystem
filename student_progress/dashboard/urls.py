from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/<int:user_id>/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/<int:user_id>/', views.resend_otp_view, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Student Management URLs
    path('students/', views.student_list_view, name='student_list'),
    path('students/add/', views.add_student_view, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student_view, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student_view, name='delete_student'),
    
    # Progress Sheet URLs
    path('progress/', views.progress_sheet_view, name='progress_sheet'),
    path('progress/add/', views.add_progress_sheet_view, name='add_progress_sheet'),
    
    # Ranking URLs
    path('ranking/', views.ranking_view, name='ranking'),
    
    # Admin URLs for adding exams and subjects
    path('exams/add/', views.add_exam_view, name='add_exam'),
    path('subjects/add/', views.add_subject_view, name='add_subject'),
]