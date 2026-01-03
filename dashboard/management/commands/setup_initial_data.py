from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Subject, Exam


class Command(BaseCommand):
    help = 'Set up initial data for the system'

    def handle(self, *args, **options):
        # Create default subjects
        subjects = ['Mathematics', 'Science', 'English', 'History', 'Geography', 'Physics', 'Chemistry', 'Biology']
        for subject_name in subjects:
            subject, created = Subject.objects.get_or_create(name=subject_name)
            if created:
                self.stdout.write(f'Created subject: {subject_name}')
            else:
                self.stdout.write(f'Subject already exists: {subject_name}')

        # Create default exams
        exams = [
            {'exam_type': 'quarterly', 'name': 'Quarterly Exam', 'date': '2026-03-15'},
            {'exam_type': 'midterm', 'name': 'Midterm Exam', 'date': '2026-06-15'},
            {'exam_type': 'model', 'name': 'Model Exam', 'date': '2026-09-15'},
            {'exam_type': 'end_term', 'name': 'End-Term Exam', 'date': '2026-12-15'},
        ]
        
        for exam_data in exams:
            exam, created = Exam.objects.get_or_create(
                exam_type=exam_data['exam_type'],
                defaults={
                    'name': exam_data['name'],
                    'date': exam_data['date']
                }
            )
            if created:
                self.stdout.write(f'Created exam: {exam_data["name"]}')
            else:
                self.stdout.write(f'Exam already exists: {exam_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial data')
        )