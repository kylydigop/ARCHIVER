from django.db import models
from taggit.managers import TaggableManager
from accounts.models import PDFBaseUser
from django.utils import timezone
import datetime
import math
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.dispatch import receiver

import os

# Create your models here.

fs = FileSystemStorage(location='/media')

class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Thesis(models.Model):
    title = models.CharField(max_length=255)
    date_submitted = models.DateTimeField(auto_now_add=True)
    abstract = models.TextField()
    uploader = models.ForeignKey(PDFBaseUser, on_delete=models.CASCADE, related_name='Uploader', null=True)
    authors = models.ManyToManyField(PDFBaseUser, related_name='Authors')
    year = models.DateField(default=datetime.date.today)
    slug = models.SlugField(null=True)

    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.uploader.userId, filename)

    document = models.FileField(upload_to=user_directory_path)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("thesis_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.date_submitted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

@receiver(models.signals.post_delete, sender=Thesis)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)
