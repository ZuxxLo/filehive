from utils.tools import extract_owner_id_from_token, convert_file_size
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
    OpenApiParameter,
)

from django.conf import settings
from jwt import decode


class FileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "search_by_title":
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

        user_id = None
        if "HTTP_AUTHORIZATION" in request.META:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            user_id = extract_owner_id_from_token(auth_header)
        if not user_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Token is invalid",
                error=True,
            )

        try:
            user = User.objects.get(id=user_id)
            files = File.objects.filter(owner=user)
            file_serializer = FileSerializer(files, many=True)
            for file_data in file_serializer.data:
                if "owner" in file_data:
                    del file_data["owner"]
            return BaseResponse(
                status_code=status.HTTP_200_OK,
                error=False,
                message="Files retreived successfully",
                data=file_serializer.data,
            )
        except Exception as e:
            return BaseResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=True,
                message=str(e),
                data=str(e),
            )

        # files = File.objects.all()
        # serializer = FileSerializer(files, many=True)
        # if not serializer.data:
        #     return BaseResponse(
        #         data=[],
        #         status_code=status.HTTP_200_OK,
        #         message="There is no files.",
        #         error=False,
        #     )
        # return BaseResponse(
        #     data=serializer.data,
        #     status_code=status.HTTP_200_OK,
        #     message="All files retrieved successfully.",
        #     error=False,
        # )

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
                    data=None,
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
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required",
                error=True,
            )

        try:

            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data=None,
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
        user_id = None
        if "HTTP_AUTHORIZATION" in request.META:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            user_id = extract_owner_id_from_token(auth_header)
        if not user_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Token is invalid",
                error=True,
            )

        file_id = pk
        if not file_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required.",
                error=True,
            )
        try:
            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_404_NOT_FOUND,
                message="File does not exist.",
                error=True,
            )
        if file_obj.owner != user_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Not the owner of the file",
                error=True,
            )

        file_obj.delete()
        return BaseResponse(
            data=None,
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
        user_id = None
        if "HTTP_AUTHORIZATION" in request.META:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            user_id = extract_owner_id_from_token(auth_header)
        if not user_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Token is invalid",
                error=True,
            )

        file_id = pk
        if not file_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="File ID is required.",
                error=True,
            )

        try:
            file_obj = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_404_NOT_FOUND,
                message="File does not exist.",
                error=True,
            )
        # Not completed
        if file_obj.owner != user_id:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Not the owner of the file",
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="The title to search for.",
                required=True,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: OpenApiResponse(
                examples=[
                    OpenApiExample(
                        name="Example",
                        value={
                            "status_code": 200,
                            "data": [
                                {
                                    "id": 6,
                                    "title": "damn",
                                    "file": "/media/files/24/05/02/275233959_2209157642570814_1372322643266469283_n_NYSKY8Z.jpg",
                                    "file_type": "jpg",
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
                                    "date_created": "2024-05-02T10:07:18.617729Z",
                                    "updated_date": "2024-05-02T10:35:01.895082Z",
                                    "file_size": "187.77 Kb",
                                }
                            ],
                            "message": "Files found successfully.",
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
    def search_by_title(self, request):
        title = request.query_params.get("title", None)
        if not title:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Title parameter is required for search.",
                error=True,
            )

        files = File.objects.filter(title__icontains=title)
        serializer = FileSerializer(files, many=True)

        if not serializer.data:
            return BaseResponse(
                data=None,
                status_code=status.HTTP_200_OK,
                message="No results found.",
                error=False,
            )

        return BaseResponse(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            message="Here are some results for your search.",
            error=False,
        )
