from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    
    class Meta:
        model = models.Student
        fields = '__all__'
    
    def validate_email(self, email):
        """
        validate if email is already exists.
        """
        if email and models.Student.objects.filter(email=email).exists():
            raise ValidationError('A student with this email is already exists.')
        return email
    
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = '__all__'
    

class SectionSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True, many=True)
    class Meta:
        model = models.Section
        fields = ['id', 'name', 'teachers', 'students']