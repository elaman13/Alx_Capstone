from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('students', views.StudentViewSet, basename='student')
router.register('courses', views.CourseViewSet, basename='course')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register('teachers', views.TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls))
]
