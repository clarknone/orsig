from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from orsig.helpers.pagination import StandardResultsSetPagination
from record import serializers, models
from record.services import create_new_commit


# Create your views here.

class RecordsView(ListCreateAPIView):
    serializer_class = serializers.RecordSerializer
    model = models.Record
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, is_committed=False).order_by('-date_created')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class RecordSingleView(RetrieveUpdateDestroyAPIView):
    models = models.Record
    serializer_class = serializers.RecordSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return self.models.objects.filter(user=self.request.user, is_committed=False).order_by('-date_created')

    def check_object_permissions(self, request, obj):
        if obj.user != request.user and request.methods not in ('GET', 'HEAD', 'OPTIONS'):
            raise PermissionDenied(detail="not only delete your records")


class CommitsView(ListCreateAPIView):
    serializer_class = serializers.CommitSerializer
    model = models.Commit
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        record_id = serializer.validated_data['record_id']
        commit_hash = serializer.validated_data['commit_hash']
        try:
            record = models.Record.objects.get(id=record_id)
            if record.user != self.request.user:
                raise PermissionDenied(detail="cannot commit another user's record")
            create_new_commit(record, commit_hash)
            record.is_committed = True
            record.save()
        except models.Record.DoesNotExist:
            raise ValidationError(detail="Record does not exist")
        except IntegrityError:
            raise ValidationError(detail="cannot commit record twice")
