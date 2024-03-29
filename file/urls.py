from django.urls import path
from .views import FileListAll,UploadViewSet
from . import views
from django.urls import path, include

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")
#...

urlpatterns = [
    #...
    path('', include(router.urls)),
 ]
# urlpatterns = [
#     path('dq/',  UploadViewSet.as_view(), name='dq'),
    
#     # path('d/', views.tttt, name='home'),
#     # path('task/', views.tutorial_list, name='tasdqsk'),

#     # path('task/', views.tutorial_list, name='task'),
#     # path('add/', views.ttt, name='ttt'),
 
# ]