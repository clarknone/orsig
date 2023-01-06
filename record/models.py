from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from orsig.helpers.generators import Generator


# Create your models here.
class Record(models.Model):
    id = models.PositiveIntegerField(default=Generator.generate_pk, primary_key=True)
    user = models.ForeignKey(get_user_model(), related_name="records", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512, blank=True)
    language = models.CharField(default="", max_length=255, blank=True)
    date_created = models.DateTimeField(default=now, blank=True)
    is_committed = models.BooleanField(default=False, blank=True)

    class Admin:
        list_display = ('title', 'description', 'language', 'date_created')
        search_fields = ('title__icontains',)


class Commit(models.Model):
    id = models.PositiveIntegerField(default=Generator.generate_pk, primary_key=True)
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=512, blank=True)
    language = models.CharField(default="", max_length=255, blank=True)
    date_created = models.DateTimeField()
    date = models.DateTimeField(blank=True)
    previous_hash = models.CharField(max_length=255, blank=True)
    commit_hash = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    is_salted = models.BooleanField(default=False, blank=True)
    hash_name = models.CharField(default="SHA256", max_length=255, blank=True)

    class Admin:
        list_display = ('title', 'previous_hash', 'hash', 'hash_name', 'is_salted', 'date')
        search_fields = ('title__icontains',)
