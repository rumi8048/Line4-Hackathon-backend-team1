from rest_framework import serializers
from .models import *

class GenreTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTag
        fields = '__all__'

class StackTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackTag
        fields = '__all__'

class UniversityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityTag
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'