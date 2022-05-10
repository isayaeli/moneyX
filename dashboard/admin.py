from django.contrib import admin
from .models import AssetBalance, DepositHistory
# Register your models here.
admin.site.register(AssetBalance)
admin.site.register(DepositHistory)