from django.urls import path
from rest_framework import routers
from . import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = router.urls