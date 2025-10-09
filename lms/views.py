from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from lms.mixins import OwnerMixin
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from usersapp.permissions import IsModer, IsOwner


class CourseViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update"]:
            return [IsAuthenticated]
        elif self.action in ["create", "destroy"]:
            return [IsAuthenticated, ~IsModer]  # модератор не может удалять/создавать
        return [IsAuthenticated]


class LessonListCreateAPIView(OwnerMixin, generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, ~IsModer]


class LessonRetrieveUpdateDestroyAPIView(OwnerMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    parser_classes = [MultiPartParser, FormParser]


    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated, ~IsModer]
        return [IsAuthenticated]
