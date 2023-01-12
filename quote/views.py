from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


class QuoteToday(RetrieveAPIView):
    serializer_class = serializers.QuoteSerializer
    permission_classes = [IsAuthenticated]
    model = models.QuoteModel

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, date_gte=now().replace(hour=0, minute=0, second=0))


class QuoteList(ListCreateAPIView):
    serializer_class = serializers.QuoteSerializer
    permission_classes = [IsAuthenticated]
    model = models.QuoteModel

    def get_queryset(self):
        return models.QuoteModel.objects.filter(user=self.request.user)


class QuoteSingle(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuoteSerializer
    permission_classes = [IsAuthenticated]
    model = models.QuoteModel
    lookup_field = "id"

    def get_queryset(self):
        return models.QuoteModel.objects.filter(user=self.request.user)
    #
    # def check_object_permissions(self, request, obj):
    #     if request.user != obj.user:
    #         raise PermissionDenied(detail={"error": "you dont have access to this resource"})
