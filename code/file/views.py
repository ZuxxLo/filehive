from .models import File
from .serializers import FileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework import status
from utils.response.base_response import BaseResponse
from filehive_auth.models import User
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from django.conf import settings

from jwt import decode


class FileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        description="Retrieve all files",
        responses={
            200: OpenApiResponse(
                description="All files retrieved successfully.",
                response=FileSerializer(many=True),
            )
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "status_code": 200,
                    "data": [
                        {
                            "id": 1,
                            "title": "file 1",
                            "file": "/media/files/24/04/23/SE2-TD5_4.pdf",
                            "owner": {
                                "id": 2,
                                "email": "rougimohamed66@gmail.com",
                                "password": "pbkdf2_sha256$720000$aVaxYZXDcC3UIznuUWZsDr$LtJifmAs4Er39T6imqEPRRivtp+8iu3SiTkDkWgAxcE=",
                                "profilePicture": "/media/user_2_moh_rougi/one.png",
                                "first_name": "moh",
                                "last_name": "rougi",
                                "is_active": True,
                                "is_verified": True,
                                "is_superuser": False,
                            },
                            "date_created": "2024-04-23T08:23:09.881000Z",
                            "updated_date": "2024-04-23T09:23:31.648000Z",
                        },
                    ],
                    "message": "All files retrieved successfully.",
                    "error": False,
                },
            )
        ],
    )
    def list(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)

        return BaseResponse(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            message="All files retrieved successfully.",
            error=False,
        )

    @extend_schema(
        request={"multipart/form-data": FileSerializer},
        responses={
            201: OpenApiResponse(
                description="All files retrieved successfully.",
                response=FileSerializer(many=True),
            )
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "status_code": 201,
                    "data": {
                        "id": 33,
                        "title": "string",
                        "file": "/media/files/24/04/26/335054233_1664520923992692_9192623840678303950_n_KCYEj4l.jpg",
                        "owner": {
                            "id": 2,
                            "email": "rougimohamed66@gmail.com",
                            "password": "pbkdf2_sha256$720000$aVaxYZXDcC3UIznuUWZsDr$LtJifmAs4Er39T6imqEPRRivtp+8iu3SiTkDkWgAxcE=",
                            "profilePicture": "/media/user_2_moh_rougi/one.png",
                            "first_name": "moh",
                            "last_name": "rougi",
                            "is_active": True,
                            "is_verified": True,
                            "is_superuser": False,
                        },
                        "date_created": "2024-04-26T16:03:38.908023Z",
                        "updated_date": "2024-04-26T16:03:38.908043Z",
                    },
                    "message": "File created successfully.",
                    "error": False,
                },
            )
        ],
    )
    def create(self, request):
        owner_id = None
        if "HTTP_AUTHORIZATION" in request.META:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            owner_id = extract_owner_id_from_token(auth_header)
        if not owner_id:
            return BaseResponse(
                data="",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Token is invalid",
                error=True,
            )

        serializer_data = request.data.copy()
        serializer_data["owner"] = owner_id
        file_extension = str(serializer_data["file"]).split(".")[
            -1
        ]  # Extract file extension
        print(file_extension)
        print("*****************")
        serializer_data["file_type"] = file_extension
        uploaded_file = request.FILES.get("file")
        file_size = convert_file_size(uploaded_file.size)
        serializer_data["file_size"] = file_size

        serializer = FileSerializer(data=serializer_data)
        if serializer.is_valid():
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

    @extend_schema(
        description="Retrieve a specific file",
        responses={
            200: OpenApiResponse(
                description="File retrieved successfully.", response=FileSerializer()
            ),
            400: OpenApiResponse(description="Bad request, invalid file ID"),
            404: OpenApiResponse(description="File not found"),
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "status_code": 200,
                    "data": {
                        "id": 33,
                        "title": "string",
                        "file": "/media/files/24/04/26/335054233_1664520923992692_9192623840678303950_n_KCYEj4l.jpg",
                        "owner": {
                            "id": 2,
                            "email": "rougimohamed66@gmail.com",
                            "password": "pbkdf2_sha256$720000$aVaxYZXDcC3UIznuUWZsDr$LtJifmAs4Er39T6imqEPRRivtp+8iu3SiTkDkWgAxcE=",
                            "profilePicture": "/media/user_2_moh_rougi/one.png",
                            "first_name": "moh",
                            "last_name": "rougi",
                            "is_active": True,
                            "is_verified": True,
                            "is_superuser": False,
                        },
                        "date_created": "2024-04-26T16:03:38.908023Z",
                        "updated_date": "2024-04-26T16:03:38.908043Z",
                    },
                    "message": "File created successfully.",
                    "error": False,
                },
            )
        ],
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

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="File deleted successfully.",
                response=FileSerializer(),
            )
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "status_code": 200,
                    "data": "",
                    "message": "File deleted successfully.",
                    "error": False,
                },
            )
        ],
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

    @extend_schema(
        examples=[OpenApiExample(name="Example", value={"title": "new title"})],
        responses={
            200: OpenApiResponse(
                examples=[
                    OpenApiExample(
                        name="Example",
                        value={
                            "status_code": 200,
                            "data": {
                                "title": "file 3",
                                "file": "/media/files/24/04/23/SE2-TD5.pdf",
                                "file_type": "pdf",
                                "owner": {
                                    "id": 2,
                                    "email": "rougimohamed66@gmail.com",
                                    "profilePicture": "/media/user_2_moh_rougi/one.png",
                                    "first_name": "moh",
                                    "last_name": "rougi",
                                    "is_active": True,
                                    "is_verified": True,
                                    "is_superuser": False,
                                },
                                "date_created": "2024-04-23T09:24:02.606000Z",
                                "updated_date": "2024-05-02T10:56:05.059703Z",
                                "file_size": "1kb",
                            },
                            "message": "File updated successfully.",
                            "error": False,
                        },
                    ),
                ],
                response={
                    "": "",
                },
            ),
        },
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


def extract_owner_id_from_token(auth_header):
    try:
        token = auth_header.split()[1]
        payload = decode(
            token,
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        )
        return payload.get("user_id", None)
    except Exception as e:
        return None


def convert_file_size(size_bytes):
    file_size_kb = size_bytes / 1024.0
    if file_size_kb >= 1024:
        file_size_mb = file_size_kb / 1024.0
        if file_size_mb >= 1024:
            file_size_gb = file_size_mb / 1024.0
            return f"{file_size_gb:.2f} GB"
        else:
            return f"{file_size_mb:.2f} MB"
    else:
        return f"{file_size_kb:.2f} Kb"
