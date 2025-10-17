from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from . import serializers
from main import models

# Create your views here.
class StudentView(generics.GenericAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name']
    ordering = ['first_name']

    def get(self, request):
        user = request.user

        # Admin can see all students
        if user.role == 'admin':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Teacher can see only students in their assigned sections
        if user.role == 'teacher':
            try:
                teacher = models.Teacher.objects.get(user=user)
                # Assuming Section has related_name='students' for Student FK
                students = models.Student.objects.filter(section__teachers=teacher)
                serializer = self.get_serializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.Teacher.DoesNotExist:
                return Response(
                    {"detail": "Teacher profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Students cannot list other students
        return Response(
            {"detail": "You do not have permission."},
            status=status.HTTP_403_FORBIDDEN
        )

    def post(self, request):
        # Only admin can create new students
        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "You do not have permission."},
            status=status.HTTP_403_FORBIDDEN
        )


class StudentDetailView(generics.GenericAPIView):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        student = self.get_object()
        print(f'request user id: {request.user.id}, student.id: {student.id}')
        if request.user.role == 'student':
            if request.user.id == student.id:
                serializer = self.get_serializer(student)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return Response(self.get_serializer(student).data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if request.user.role == 'admin':
            student = self.get_object()
            student.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class SectionView(generics.GenericAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get(self, request):
        """
        Admin: Get all Sections.
        Teachers: Only get assigned sections.
        """
        user = request.user

        # Admin view
        if user.role == 'admin':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Teachers view
        elif user.role == 'teacher':
            try:
                teacher = models.Teacher.objects.get(user=user)
                classes = teacher.classes.all()
                serializer = self.get_serializer(classes, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.Teacher.DoesNotExist:
                return Response(
                    {"error": "Teacher profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        # Student or unauthorized user
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request):
        """
        Admin: Post a new Section. (only admin can do it.)
        """
        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class SectionDetailView(generics.GenericAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        section = get_object_or_404(self.get_queryset(), pk=pk)

        if user.role == 'admin':
            serializer = self.get_serializer(section)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif user.role == 'teacher':
            is_assigned = section.teachers.filter(user=user).exists()
            if is_assigned:
                serializer = self.get_serializer(section)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "You are not assigned to this section."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, pk):
        user = request.user
        if user.role == 'admin':
            section = self.get_object()
            serializer = self.get_serializer(section, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        user = request.user
        if user.role == 'admin':
            section = self.get_object()
            section.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class CourseView(generics.GenericAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'credit_hour']
    ordering_fields = ['title']
    ordering = ['title']

    def get(self, request):

        if request.user.role == 'admin':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):

        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class CourseDetailView(generics.GenericAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        course = self.get_object()

        if user.role == 'admin':
            serializer = self.get_serializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk):
        course = self.get_object()
        user = request.user

        if user.role == 'admin':
            serializer = self.get_serializer(course, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        if request.user.role == 'admin':
            course = self.get_object()
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class GradeView(generics.GenericAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['student__first_name', 'student__last_name', 'course__name']
    ordering_fields = ['points', 'date']
    ordering = ['date']


    def get(self, request):
        grades = self.get_queryset()

        # Get all grades
        if request.user.role == 'admin':
            serializer = self.get_serializer(grades, many=True)           
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Get if the teacher teaches that course
        elif request.user.role == 'teacher':
            teacher = get_object_or_404(models.Teacher, user=request.user)
            filtered_grades = grades.filter(course__in=teacher.courses.all())
            serializer = self.get_serializer(filtered_grades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Get enrolled course grades only
        elif request.user.role == 'student':
            student = self.get_queryset().filter(student__user=request.user)
            serializer = self.get_serializer(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):
        
        # only Admin can Post
        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)    


class GradeDetailView(generics.GenericAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        grade = self.get_object()

        if user.role == 'admin':
            serializer = self.get_serializer(grade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif user.role == 'teacher' and self.get_object().course.assigned_teacher.user == request.user:
            serializer = self.get_serializer(grade) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif user.role == 'student' and grade.student.user == user:
            serializer = self.get_serializer(grade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk):
        grade = self.get_object()

        if request.user.role == 'admin':
            serializer = self.get_serializer(grade, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.user.role == 'teacher' and grade.course.assigned_teacher.user == request.user:
            points = {"points": request.data.get("points")}
            serializer = self.get_serializer(grade, data=points, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK) 
        

        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        if request.user.role == 'admin':
            grade = self.get_object()
            grade.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class TeacherView(generics.GenericAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name']
    ordering = ['first_name']


    def get(self, request):

        if request.user.role == 'admin':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request):

        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)


class TeacherDetailView(generics.GenericAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        teacher = self.get_object()

        if user.role == 'admin' or (user.role == 'teacher' and teacher.user == user):
            serializer = self.get_serializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk):
        teacher = self.get_object()
        user = request.user

        if user.role == 'admin' or (user.role == 'teacher' and teacher.user == user):
            serializer = self.get_serializer(teacher, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        if request.user.role == 'admin':
            teacher = self.get_object()
            teacher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)