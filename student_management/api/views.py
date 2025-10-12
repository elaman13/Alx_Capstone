from rest_framework.viewsets import ModelViewSet
from . import serializers
from main import models

# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class EnrollmentViewSet(ModelViewSet):
    queryset = models.Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer

class TeacherViewSet(ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer