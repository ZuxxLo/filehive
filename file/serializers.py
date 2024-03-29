from rest_framework  import serializers
from rest_framework.serializers  import  FileField

from .models import File

class FileSerializer(serializers.ModelSerializer): 
    file_uploaded = FileField()
  
    class Meta:
        model = File
        fields = ('_id', 'title', 'file_uploaded', 'owner')