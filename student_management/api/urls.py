from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from main import views as main_views

router = DefaultRouter()

router.register('students', views.StudentViewSet, basename='student')
router.register('courses', views.CourseViewSet, basename='course')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register('teachers', views.TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', main_views.LoginView.as_view()),
    path('signup/', main_views.SignUpView.as_view())
]
