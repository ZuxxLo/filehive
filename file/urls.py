from django.urls import path
from .views import FileViewSet
from . import views
from django.urls import path, include

from rest_framework import routers
router = routers.DefaultRouter()
router.register('', FileViewSet, basename="")
#...

urlpatterns = [
    #...
    path('', include(router.urls)),
 ]
# urlpatterns = [
#     path('dq/',  FileViewSet.as_view(), name='dq'),
    
#     # path('d/', views.tttt, name='home'),
#     # path('task/', views.tutorial_list, name='tasdqsk'),

#     # path('task/', views.tutorial_list, name='task'),
#     # path('add/', views.ttt, name='ttt'),
 
# ]
urlpatterns = [
    #only to test in documentation
    path(
        '',  
        FileViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='',
    ),
    path(
        'id/<str:pk>/',  
        FileViewSet.as_view({'get': 'retrieve','put': 'update', 'delete': 'destroy'}),#, 
        name='file_detail',
    ),


    #actual working urls
    path(
        'create/',
        FileViewSet.as_view({'post': 'create'}),
        name='create',
    ),
    path(
        'list/',
        FileViewSet.as_view({'get': 'list'}),
        name='list',
    ),
    path(
        'retrieve/<str:pk>/',
        FileViewSet.as_view({'get': 'retrieve'}),
        name='retrieve',
    ),   
    path(
        'destroy/<str:pk>/',
        FileViewSet.as_view({'delete': 'destroy'}),
        name='destroy',
    ),
     path(
        'update/<str:pk>/',
        FileViewSet.as_view({'put': 'update'}),
        name='update',
    ),         

]