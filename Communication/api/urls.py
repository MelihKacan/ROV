from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("post_request",views.post_request,name="post_request"),
    path("camera",views.camera_stream,name="camera"),
    path("camera-feed",views.shape_page,name="camera-feed"),
    path("get_request",views.get_request,name="get_request"),
]
