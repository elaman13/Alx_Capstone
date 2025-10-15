from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, permissions as custom_permission
from rest_framework.exceptions import ErrorDetail
from main import models

# Create your views here.
class StudentView(generics.GenericAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if  request.user.role == 'admin':
            pass

        if request.user.role == 'teacher':
            serializer = self.get_serializer(self.get_queryset(), many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


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

            return Response(status=status.HTTP_404_NOT_FOUND)
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
                teacher = models.Teacher.objects.get(pk=user.id)
                classes = teacher.classes.all()
                serializer = self.get_serializer(classes, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.Teacher.DoesNotExist:
                return Response(
                    {"error": "Teacher profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        # Student or unauthorized user
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request):
        """
        Admin: Post a new Section. (only admin can do it.)
        """
        if request.user.role == 'admin':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

class SectionDetailView(generics.GenericAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer

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
        
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, pk):
        user = request.user
        if user.role == 'admin':
            section = self.get_object()
            serializer = self.get_serializer(section, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        user = request.user
        if user.role == 'admin':
            section = self.get_object()
            section.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class GradeViewSet(ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer

class TeacherViewSet(ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer