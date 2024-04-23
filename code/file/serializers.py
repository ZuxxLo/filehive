from rest_framework import serializers
from rest_framework.serializers import FileField

from .models import File

from filehive_auth.serializers import UserSerializer

from filehive_auth.models import User


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ("id", "title", "file", "owner", "date_created", "updated_date", "file_type")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        owner_id = response.get("owner")
        owner = User.objects.get(id=owner_id)
        response["owner"] = UserSerializer(owner).data
        return response

    def update(self, instance, validated_data):
        # Remove owner field from validated data
        validated_data.pop("owner", None)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Ensure 'id' field is not provided by the user
        validated_data.pop("id", None)

        return super().create(validated_data)
