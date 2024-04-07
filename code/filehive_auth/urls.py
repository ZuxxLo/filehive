from django.urls import path
from .views import RegisterView, LoginView, VerifyAccountView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('verify/<uidb64>/<token>', VerifyAccountView.as_view(), name='verify')
    

]
