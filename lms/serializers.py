from rest_framework import serializers

from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'description', 'preview', 'video_url')
        read_only_fields = ('id',)

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons', 'lessons_count')
        read_only_fields = ('id',)

