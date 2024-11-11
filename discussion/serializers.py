from rest_framework import serializers
from .models import Discussion
from .models import Image

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'
        