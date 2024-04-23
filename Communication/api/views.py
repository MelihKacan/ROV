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
        
        if serializer_rotary.is_valid():
            existing_data = data.objects.filter(id=1).first()
            if existing_data:
                serializer_rotary.update(existing_data, serializer_rotary.validated_data)
            else:
                serializer_rotary.save()
                return Response(status=status.HTTP_200_OK)

        if serializer_joyistik.is_valid():
            existing_data = data.objects.filter(id=2).first()
            if existing_data:
                serializer_joyistik.update(existing_data, serializer_joyistik.validated_data)
            else:
                serializer_joyistik.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
