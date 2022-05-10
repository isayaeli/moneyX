from datetime import datetime
from itertools import chain
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

class DepositHistory(models.Model):
    history = models.JSONField(null=True)
    saved_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.saved_on)

    class Meta:
        verbose_name_plural = 'Deposit History'