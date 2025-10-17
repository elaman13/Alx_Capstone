from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
    
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.first_name


class Section(models.Model):
    name = models.PositiveIntegerField()
    teachers = models.ManyToManyField(Teacher, related_name='classes', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
    email = models.EmailField(blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    
    
    def __str__(self):
        return self.first_name

class Course(models.Model):    
    title = models.CharField(max_length=255)
    credit_hour = models.PositiveIntegerField()
    students = models.ManyToManyField(Student, through='Grade', related_name='courses')
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return self.title

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    points = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f'{self.student.first_name}, {self.course.title}'