from datetime import datetime
from tabnanny import verbose
from django.db import models

# Create your models here.
class AssetBalance(models.Model):
    balance = models.CharField(max_length=255, null=True, default=0)
    changed_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.balance

    class Meta:
        verbose_name_plural = 'Asset balance'