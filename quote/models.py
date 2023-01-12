from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

# Create your models here.

User = get_user_model()


class QuoteModel(models.Model):
    user = models.ForeignKey(User, related_name="qoutes", on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    date = models.DateTimeField(default=now, blank=True)
    meta = models.CharField(max_length=512, default="")
