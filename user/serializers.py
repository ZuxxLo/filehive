from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('_id', 'firstName', 'lastName', 'email', 'password', 'picture', 'verified', 'active')