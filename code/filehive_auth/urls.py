from django.urls import path
from .views import RegisterView, LoginView, VerifyAccountView, VerifyEmail,SendResetEmail, ResetPasswordView, ResetEmail, VerifyReset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/verify/<uidb64>/<token>', VerifyAccountView.as_view(), name='verify'),
    path("email-verified/<uidb64>/<token>", VerifyEmail.as_view(), name="email-verified" ),
    path("auth/receive-reset", SendResetEmail.as_view()),
    path('auth/reset/<uidb64>/<token>', VerifyReset.as_view(), name='verify-reset'),
    path("reset-password/<uidb64>/<token>", ResetEmail.as_view(), name="reset-password"),
    path("auth/reset", ResetPasswordView.as_view(), name='reset' )

]
