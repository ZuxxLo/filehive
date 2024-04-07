from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User

from .serializers import UserSerializer
from .serializers import MyTokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

# for sending mails and generate token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render


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
# sign-up code
class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate token for sending mail
        email_subject = "Verify Your Account"
        message= render_to_string(
            "registration/verify.html",
           {
            'user':user,
            'domain': 'localhost:3000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
           }

        )
     
        email_message = EmailMessage(
                email_subject, message ,settings.EMAIL_HOST_USER, to=[user.email]
            )
        email_message.content_subtype = 'html'
        email_message.send()
        return Response({'message': 'User registration successful!', 'user': serializer.data}, status=status.HTTP_201_CREATED)
   

class VerifyEmail(APIView):
    def get(self, request, uidb64, token):
        print("message sent")

class VerifyAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid= force_text(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_verified = True
            user.save()
            return Response({
                'message': f'User {user.get_full_name()} with email: {user.email} is verified',
                'status':'success'
                 
            }, status=status.HTTP_200_OK)
        else:
               return Response({
                'message': f'User {user.get_full_name()} is not verified',
                'status': 'failed'
             
            }, status=status.HTTP_403_FORBIDDEN)

# Login code
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
        if not user.is_verified:
            email_subject = "Verify Your Account"
            message = render_to_string(
                "registration/verify.html",
                {
                    'user': user,
                    'domain': 'localhost:3000',  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
            )
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, to=[user.email]
            )
            email_message.content_subtype = 'html'
            email_message.send()

            return Response({'message': 'user not verified. Verification email sent. Please Verify Your email and Login Again'}, status=status.HTTP_403_FORBIDDEN)

        tokens = MyTokenObtainPairSerializer.get_token(user)  # Get tokens directly
        refresh = str(tokens)
        access = str(tokens.access_token)
        # type = tokens.access_token.token_type
        # type = tokens.token_type for refresh type
        serializer = UserSerializer(user)
        user_data = serializer.data
        return Response({
                'message': 'Login User Successful!',
                'user': user_data,
                'refresh_access': refresh,
                'acess_token': access,  # Unpack tokens into the response
            }, status=status.HTTP_200_OK)
# Reset Password Section


class SendResetEmail(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not Found!")
        email_subject = "Reset Your Password"
        message = render_to_string(
                "registration/reset.html",
                {
                    'user': user,
                    'domain': 'localhost:3000',  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
            )
        email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, to=[user.email]
            )
        email_message.content_subtype = 'html'
        email_message.send()
        return Response({
            "message": f'Reset Password email was sent to this email: {user.email}'
        })
class VerifyReset(APIView):
   def post(self, request, uidb64, token):
        try:
            uid= force_text(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
     
            return Response({
                'message': f'Now You can Change password',
                'status':'success'
                 
            }, status=status.HTTP_200_OK)
        else:
               return Response({
                'message': f'there was an error',
                'status': 'failed'
             
            }, status=status.HTTP_400_BAD_REQUEST)


class ResetEmail(APIView):
    def get(self, request, uidb64, token):
        print("message sent")


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        newPassword = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not Found!")
        if not user.is_verified:
            email_subject = "Verify Your Account"
            message = render_to_string(
                "registration/verify.html",
                {
                    'user': user,
                    'domain': 'localhost:3000',  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
            )
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, to=[user.email]
            )
            email_message.content_subtype = 'html'
            email_message.send()
            return Response({'message': 'user not verified. Verification email sent. Please Verify Your email and Login Again'}, status=status.HTTP_403_FORBIDDEN)

        if newPassword is not None :
            user.set_password(newPassword)
            user.save()
            serializer = UserSerializer(user)
            user_data = serializer.data
            return Response({
                 'message': 'Reset Password was Successful',
                 'user': user_data,
                 'status': 'success'  # Unpack tokens into the response
             }, status=status.HTTP_200_OK)
        else:
            return  Response({"Error": "Please Provide a New Password"}, status=status.HTTP_400_BAD_REQUEST)

    


