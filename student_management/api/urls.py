from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from main import views as main_views


urlpatterns = [
    path('login/', main_views.LoginView.as_view(), name='login'),
    path('signup/', main_views.SignUpView.as_view(), name='signup'),
    path('students/', views.StudentView.as_view(), name='students'),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='students-detail'),
    path('sections/', views.SectionView.as_view(), name='sections'),
    path('sections/<int:pk>/', views.SectionDetailView.as_view(), name='section-detail'),
    path('grades/', views.GradeView.as_view(), name='grades'),
    path('grades/<int:pk>/', views.GradeDetailView.as_view(), name='grades'),
    path('teachers/', views.TeacherView.as_view(), name='teachers'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('courses/', views.CourseView.as_view(), name='courses'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail')
]
