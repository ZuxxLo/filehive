from rest_framework  import serializers
from rest_framework.serializers  import  FileField

from .models import File
from user.serializers import UserSerializer
from user.models import User

class FileSerializer(serializers.ModelSerializer): 
    owner = UserSerializer() 
    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'owner','date_created','updated_date')
    def update(self, instance, validated_data):
        # Ensure 'id' and 'owner' fields are not modified
        if 'id' in validated_data or 'owner' in validated_data:
            raise serializers.ValidationError("Cannot update 'id' or 'owner' fields.")
        
        return super().update(instance, validated_data)        

    def create(self, validated_data):
        # Ensure 'id' field is not provided by the user
        validated_data.pop('id', None)
        
        return super().create(validated_data)