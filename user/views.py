from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view


# Create your views here.

class UserListAll(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer