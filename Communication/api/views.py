from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import DataSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import data

def index(request):
    return render(request,"index.html")

"""@api_view(['POST'])
def post_request(request):
    if request.method == 'POST':
        serializer = DataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)"""
            
@api_view(['POST'])
def post_request(request):
    if request.method == 'POST':
        received_data_rotary = {"value":request.data["rotary"]}
        
        received_data_joyistik = {"value":request.data["joyistik"]}
        
        serializer_rotary = DataSerializer(data=received_data_rotary)
        
        serializer_joyistik = DataSerializer(data=received_data_joyistik)
        
        if serializer_rotary.is_valid() and serializer_joyistik.is_valid():
            existing_data = data.objects.filter(id=1).first()
            existing_data2 = data.objects.filter(id=2).first()
            if existing_data and existing_data2:
                serializer_rotary.update(existing_data, serializer_rotary.validated_data)
                serializer_joyistik.update(existing_data2, serializer_joyistik.validated_data)
                return Response(status=status.HTTP_200_OK)
            else:
                serializer_rotary.save()
                serializer_joyistik.save()
                return Response(status=status.HTTP_200_OK)

        """if serializer_joyistik.is_valid():
            existing_data = data.objects.filter(id=2).first()
            if existing_data:
                serializer_joyistik.update(existing_data, serializer_joyistik.validated_data)
                return Response(status=status.HTTP_200_OK)
            else:
                serializer_joyistik.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)"""

@api_view(['GET'])
def get_request(request):
    if request.method == 'GET':
        all_rotary_data = data.objects.all().filter(id=1).first()
        all_joystick_data = data.objects.all().filter(id =2).first()
        all_data = all_rotary_data , all_joystick_data
        serializer = DataSerializer(all_data,many=True)
        return Response(serializer.data)

from django.http import StreamingHttpResponse
from .shape_detection_mode import gen_frames

def camera_stream(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def shape_page(request):
    return render(request,"camera.html")

from .autonomous_mode import mission

def autonomous_stream(request):
    return StreamingHttpResponse(mission("blue"), content_type='multipart/x-mixed-replace; boundary=frame')

def autonomous_page(request):
    return render(request,"autonomous_page.html")