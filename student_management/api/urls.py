from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from main import views as main_views

router = DefaultRouter()

router.register('courses', views.CourseViewSet, basename='course')
router.register('enrollments', views.GradeViewSet, basename='enrollment')
router.register('teachers', views.TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', main_views.LoginView.as_view(), name='login'),
    path('signup/', main_views.SignUpView.as_view(), name='signup'),
    path('students/', views.StudentView.as_view(), name='students'),
    path('profile/students/<int:pk>', views.StudentDetailView.as_view(), name='students-detail'),
    path('sections/', views.SectionView.as_view(), name='sections'),
    path('sections/<int:pk>/', views.SectionDetailView.as_view(), name='section-detail')
]
