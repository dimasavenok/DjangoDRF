from django.urls import path
from rest_framework import routers
from . import views


from rest_framework.routers import DefaultRouter

from .views import PaymentListView

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path("payments/", PaymentListView.as_view(), name="payments-list"),
]