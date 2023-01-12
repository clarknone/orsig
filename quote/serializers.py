from rest_framework.serializers import ModelSerializer
from .models import QuoteModel


class QuoteSerializer(ModelSerializer):
    class Meta:
        fields = ["text", "date", 'id']
        model = QuoteModel
