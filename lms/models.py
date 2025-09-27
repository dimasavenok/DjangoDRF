from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses_previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='lessons_previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} ({self.course})'
