from datetime import datetime
from django.contrib.auth.models import User
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
    STATUS =  (
        ('succesful','successful'),
        ('not-successful','not-successful')
    )
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    history = models.JSONField(null=True)
    status =  models.CharField(choices=STATUS, max_length=50,default='not-successful')
    saved_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.saved_on)

    class Meta:
        verbose_name_plural = 'Deposit History'



class Deposit(models.Model):
    user  = models.ForeignKey(User, related_name='userdeposit', on_delete=models.CASCADE)
    balance = models.DecimalField( max_digits=255, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    chain = models.CharField(max_length=255)
    verify = models.BooleanField(default=False)
    initiated_on = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return str(self.user)



class BinaryWithDraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)
    
    

