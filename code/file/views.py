from .models import File
from .serializers import FileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework import status
from utils.response.base_response import BaseResponse
from filehive_auth.models import User


class FileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def list(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)

        return BaseResponse(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            message="All files retrieved successfully.",
            error=False,
        )

    def create(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            owner_id = request.data.get("owner", None)
            if not owner_id:

                return BaseResponse(
                    data="",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Owner ID is required.",
                    error=True,
                )

            try:
                owner = User.objects.get(id=owner_id)
            except User.DoesNotExist:
                return BaseResponse(
                    data="",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Owner does not exist.",
                    error=True,
                )

            serializer.save()

            return BaseResponse(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
                message="File created successfully.",
                error=False,
            )

        return BaseResponse(
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer.errors,
            error=True,
        )

    def retrieve(self, request, pk=None):
        file_id = pk
        if not file_id:
            return BaseResponse(
                data="",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required",
                error=True,
            )

        try:

            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data="",
                status_code=status.HTTP_404_NOT_FOUND,
                message="File does not exist.",
                error=True,
            )
        serializer = FileSerializer(file_obj)
        return BaseResponse(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            message="File retrieved successfully.",
            error=False,
        )

    def destroy(self, request, pk=None):
        file_id = pk
        if not file_id:
            return BaseResponse(
                data="",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required.",
                error=True,
            )
        try:
            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data="",
                status_code=status.HTTP_404_NOT_FOUND,
                message="File does not exist.",
                error=True,
            )

        file_obj.delete()
        return BaseResponse(
            data="",
            status_code=status.HTTP_200_OK,
            message="File deleted successfully.",
            error=False,
        )

    def update(self, request, pk=None):
        file_id = pk
        if not file_id:
            return BaseResponse(
                data="",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required.",
                error=True,
            )

        try:
            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data="",
                status_code=status.HTTP_404_NOT_FOUND,
                message="File does not exist.",
                error=True,
            )

        # Check if 'title' field is provided
        # if "title" not in request.data:
        #     return BaseResponse(
        #         data="",
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         message="Title field is required.",
        #         error=True,
        #     )

        serializer = FileSerializer(file_obj, data=request.data, partial=True)
        if "id" in serializer.fields:
            del serializer.fields["id"]
        # Check if 'title' field is present and not empty in the request data
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return BaseResponse(
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                message="File updated successfully.",
                error=False,
            )
        return BaseResponse(
            data="",
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer.errors,
            error=True,
        )
