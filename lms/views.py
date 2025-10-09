from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.mixins import OwnerMixin
from lms.models import Course, Lesson, Subscription
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

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        sub, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if created:
            serializer = CourseSerializer(course, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Уже подписан."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        deleted, _ = Subscription.objects.filter(user=request.user, course=course).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Подписка не найдена."}, status=status.HTTP_404_NOT_FOUND)


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
