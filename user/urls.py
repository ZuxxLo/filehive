from django.urls import path
from .views import UserListAll

urlpatterns = [
    path('', UserListAll.as_view(), name='home'),
]