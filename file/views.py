from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
 
# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = FileSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        tut = FileSerializer(data=request.data)
   
        if tut.is_valid():
            tut.save()    
        return Response(tut.data)
    


class FileListAll(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
 

@api_view(['POST'])
def tttt(request):
    tut = FileSerializer(data=request.data)
   
    if tut.is_valid():
            tut.save()
            return Response(tut.data) 
    return Response(tut.errors)
 
@api_view(['GET'])
def tutorial_list(request):
    queryset = File.objects.all()
    serializer= FileSerializer(queryset, many= True)
    return Response(serializer.data)  


@api_view(['POST'])
def ttt(request):
    tut = FileSerializer(data=request.data)
   
    if tut.is_valid():
            tut.save()
            return Response(tut.data) 
    return Response(tut.errors)

 