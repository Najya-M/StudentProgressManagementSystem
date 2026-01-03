# Student Progress Management System

A Django-based application for managing student information and academic progress.

## Features

- User authentication with email OTP verification
- Student management (CRUD operations)
- Progress tracking for different exam types (Quarterly, Midterm, Model, End-Term)
- Subject and exam management
- Student ranking based on exam performance
- Search and filter functionality

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install django
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the admin panel at `/admin/` to manage the system
2. Register as a new user or login with existing credentials
3. Use the dashboard to manage students and their progress

## Admin Credentials

- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

## Technology Stack

- Backend: Python Django
- Database: SQLite (default Django DB)
- Frontend: Django Templates (HTML, CSS)
- Authentication: Django Auth + Email OTP verification

## Modules

1. Authentication Module
   - User registration with email OTP verification
   - Secure login system

2. Admin Dashboard
   - Student management (CRUD)
   - Progress tracking
   - Ranking system

3. Progress Sheet Module
   - Marks entry for different exam types
   - Subject management

4. Ranking & Filtering
   - Sort students by exam performance
   - Filter by exam type