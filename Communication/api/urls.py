from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("post_request",views.post_request,name="post_request"),
]
