from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)


User = get_user_model()


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    
    email = models.EmailField(blank=True, null=True, unique=True)
    
    
    def __str__(self):
        return self.first_name

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    
    email = models.EmailField(blank=True, null=True)
    
    def __self__(self):
        return self.first_name

class Course(models.Model):
    CREDIT_HOUR = [(i, str(i)) for i in range(1, 101)]
    
    title = models.CharField(max_length=255)
    credit_hour = models.IntegerField(choices=CREDIT_HOUR)
    students = models.ManyToManyField(Student, through='Enrollment', related_name='courses')
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    date = models.DateField()
    
    def __str__(self):
        return f'{self.student.first_name}, {self.course.title}'
