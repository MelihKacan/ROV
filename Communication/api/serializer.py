from rest_framework import serializers
from .models import data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = ['id', 'value','name']
        extra_kwargs = {"id":{"read_only" :  True}}
    
    def create_data(self,validated_data):
        data1 = data(
            value = validated_data["value"],
        )   
        data1.save()
        return data1