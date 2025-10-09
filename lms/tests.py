from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription

User = get_user_model()

class LessonCRUDAndSubscriptionTests(APITestCase):
    def setUp(self):
        # пользователи
        self.user_owner = User.objects.create_user(email="owner@example.com", password="pass1234")
        self.user_other = User.objects.create_user(email="other@example.com", password="pass1234")
        self.moderator = User.objects.create_user(email="mod@example.com", password="pass1234")
        # группа модераторов
        mod_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(mod_group)

        # создать курс
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_owner)
        self.course = Course.objects.create(title="Test Course", owner=self.user_owner)

        # создать урок (владелец)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, owner=self.user_owner)

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("lesson-list")
        data = {"title": "New Lesson", "course": self.course.id, "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        resp = self.client.post("/api/lessons/", data, format='json')
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED,))
        self.assertEqual(Lesson.objects.filter(title="New Lesson").count(), 1)
        created = Lesson.objects.get(title="New Lesson")
        self.assertEqual(created.owner, self.user_owner)

    def test_other_cannot_edit_owner_lesson(self):
        self.client.force_authenticate(user=self.user_other)
        url = f"/api/lessons/{self.lesson.id}/"
        resp = self.client.patch(url, {"title": "Hacked"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_edit_but_not_delete(self):
        self.client.force_authenticate(user=self.moderator)
        url = f"/api/lessons/{self.lesson.id}/"
        resp = self.client.patch(url, {"title": "Edited by moderator"}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Edited by moderator")

        resp2 = self.client.delete(url)
        self.assertIn(resp2.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_401_UNAUTHORIZED))

    def test_subscription_create_and_flag(self):
        self.client.force_authenticate(user=self.user_other)
        subscribe_url = f"/api/courses/{self.course.id}/subscribe/"
        resp = self.client.post(subscribe_url)
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        self.assertTrue(Subscription.objects.filter(user=self.user_other, course=self.course).exists())


        course_detail = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertEqual(course_detail.status_code, status.HTTP_200_OK)
        self.assertTrue(course_detail.data.get("is_subscribed"))

        resp2 = self.client.delete(f"/api/courses/{self.course.id}/unsubscribe/")
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user_other, course=self.course).exists())

    def test_video_validator_rejects_non_youtube(self):
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.post("/api/lessons/", {"title": "Bad link", "course": self.course.id, "video_url": "https://some-edu.com/video/123"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("video_url", resp.data)