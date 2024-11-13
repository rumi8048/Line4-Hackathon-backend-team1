from rest_framework import serializers
from ptn_project.models import AIFeedbackSummary
from .models import *


class AiSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFeedbackSummary
        fields = '__all__'