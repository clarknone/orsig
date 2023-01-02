from rest_framework import serializers
from . import models


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'description', 'id', 'language']
        read_only_fields = ['id']
        model = models.Record


class CommitSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        fields = ['previous_hash', 'hash', 'record_id', 'commit_hash', 'title', 'description', 'id', 'language']
        model = models.Commit
