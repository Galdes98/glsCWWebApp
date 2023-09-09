from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name= 'home'),
    path('sign-up', views.sign_up, name= 'sign_up'),
    path('create-post', views.create_post, name= 'create_post'),
    path('webcam/', views.webcam_view.as_view(), name='webcam'),
    path('take-picture/', views.takePicture, name='picture'),
    path('download-history/', views.downloadHistory, name='history'),    
    path('boot-test/', views.bootTest, name='boot_test'),
]

