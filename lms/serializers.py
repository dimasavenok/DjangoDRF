from rest_framework import serializers

from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'description', 'preview', 'video_url', 'order')
        read_only_fields = ('id',)

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons')
        read_only_fields = ('id',)

