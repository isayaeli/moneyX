from datetime import datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    currency = models.CharField(max_length=100)
    deposited_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user



class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    currency = models.CharField(max_length=100)
    fee = models.IntegerField()
    withdrawn_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user