# Student Management API

This project is a simple API for managing student, teacher, course, section and grade. It is build with Django and Django REST Framework. The API have role based acces control, so users can see only what they allowed.

Features

### Students

- Admin can create, list, update, delete students.

- Teachers can see students only in they assigned sections.

- Students can see only their own info.

### Teachers

- Admin can manage all teachers.

- Teacher can see and update only they profile.

### Courses

- Admin can create and manage courses.

- Only admin can see courses.

### Sections

- Admin can manage all sections.

- Teacher can see only sections they assigned.

- Students can not see sections directly.

### Grades

- Admin can create and manage grades.

- Teacher can update grades only in their courses.

- Students can see only their own grades.

### Searching and ordering

- Some views support searching and ordering (like students, teachers, courses, grades) using query params.

### Role based permissions

- Every request check the user role (admin, teacher, student) and give acces accordly.

## API Endpoints
1. *Register User*
   - *POST* /api/signup/
   -  *Request Body:*
     json
     {
       "username": "Abi"
       "email": "abi@gmail.com"
       "password" "Abi@2025"
     }
    - *Response:*
     json
     {
       "message": "User registered successfully"
     }

     
- /api/students/ - list or create students

- /api/students/[id]/ - get, update, delete student

- /api/teachers/ - list or create teachers

- /api/teachers/[id]/ - get, update, delete teacher

- /api/courses/ - list or create courses

- /api/courses/[id]/ - get, update, delete course

- /api/sections/ - list or create sections

- /api/sections/[id]/ - get, update, delete section

- /api/grades/ - list or create grades

- /api/grades/[id]/ - get, update, delete grade

## Installation

#### Clone the project

- git clone https://github.com/yourusername/student-api.git
- cd student-api

## Migrate database

- python manage.py makemigrations main
- python manage.py migrate
- python manage.py runserver

## Open in browser

- http://127.0.0.1:8000/api

## Notes

- You need login to acces most endpoints.

- Searching example: /api/students/?search=biruk

- Ordering example: /api/students/?ordering=first_name

- Role based access is important, student cannot see other student, teacher cannot delete students.
