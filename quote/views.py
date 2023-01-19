from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orsig.helpers.pagination import StandardResultsSetPagination
from . import models
from . import serializers


class QuoteToday(APIView):
    serializer_class = serializers.QuoteSerializer
    permission_classes = [IsAuthenticated]
    model = models.QuoteModel

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, date__gte=now().replace(hour=0, minute=0, second=0))

    def get(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        if data:
            data = self.serializer_class(data)
            return Response(data.data)
        raise NotFound(detail="No quote available for today")


class QuoteList(ListCreateAPIView):
    serializer_class = serializers.QuoteSerializer
    permission_classes = [IsAuthenticated]
    model = models.QuoteModel
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return models.QuoteModel.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


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
