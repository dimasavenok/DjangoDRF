from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from rest_framework import generics, filters

# Create your views here.
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema(tags=["Payments"])
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]
    search_fields = ["method"]
