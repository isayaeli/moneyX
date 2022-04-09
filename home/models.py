from datetime import datetime
from django.db import models
from datetime import datetime

# Create your models here.
class Notification(models.Model):
    message = models.TextField()
    recieved_on =  models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.recieved_on



class Ad(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ads_images',null=True, blank=True)
    video = models.FileField(upload_to='ads_videos',null=True, blank=True)
    details = models.TextField()

    def __str__(self):
        return self.title