from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

# from bson import ObjectId
import re
from response.base_response import BaseResponse

from filehive_auth.models import User
from rest_framework.views import APIView


def is_valid_objectid(file_id):
    """
    Checks if the provided string is a valid ObjectId.
    """
    return True
    # return bool(re.match(r'^[0-9a-fA-F]{24}$', file_id))


# ViewSets define the view behavior.


# def get_permissions(self):
#     # check the action and return the permission class accordingly
#     if self.action == "create":
#         return [
#             # IsAdminUser(),
#         ]
#     return [
#         IsAuthenticated(),
#     ]


class FileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def list(self, request):

        # auth_header = request.META.get("HTTP_AUTHORIZATION")
        # if not auth_header:
        #     raise AuthenticationFailed("the authorization header was not provided!.")
        # parts = auth_header.split(" ")
        # if parts[0].lower() != "bearer":
        #     raise AuthenticationFailed("Invalid authentication header. Use Bearer.")
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

        serializer = FileSerializer(file_obj, data=request.data, partial=True)
        if "id" in serializer.fields:
            del serializer.fields["id"]

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
