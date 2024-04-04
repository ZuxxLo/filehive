from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','email',  'password', 'first_name', 'last_name', 'is_active', 'is_verified']
    

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
      
        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):


    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
  
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['profilePicture'] = str(user.profilePicture)
        token['is_verified'] = user.is_verified
        token['is_active'] = user.is_active
    
        return token