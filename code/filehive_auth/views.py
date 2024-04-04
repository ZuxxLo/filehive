from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User

from .serializers import UserSerializer
from .serializers import MyTokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter








class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(
    parameters=[
        OpenApiParameter('email', required=True, description='Email address', type=str),
        OpenApiParameter('password', required=True, description='Password', type=str),
        OpenApiParameter('first_name', required=True, description='First name', type=str),  # Added line for first_name
        OpenApiParameter('last_name', required=True, description='Last name', type=str), 
    ],
    responses={
        200: 'User Details',
        400: 'Bad request',
    },
)
class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registration successful!', 'user': serializer.data}, status=status.HTTP_201_CREATED)



@extend_schema(
    parameters=[
        OpenApiParameter('email', required=True, description='Email address'),
        OpenApiParameter('password', required=True, description='Password'),
    ],
    responses={
        200: 'Token response',
        400: 'Bad request',
    },
)
class LoginView(APIView):

    def post(self, request):
   
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()


        if user is None:
            raise AuthenticationFailed("User not Found!")
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
     
        tokens = MyTokenObtainPairSerializer.get_token(user)  # Get tokens directly
        refresh = str(tokens)
        access = str(tokens.access_token)
        # type = tokens.access_token.token_type
        # type = tokens.token_type for refresh type
        return Response({
                'message': 'Login User Successful!',
                'refresh_access': refresh,
                'acess_token': access,  # Unpack tokens into the response
            }, status=status.HTTP_200_OK)
        