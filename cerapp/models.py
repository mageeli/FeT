from django.db import models
from django.urls import reverse


class Post(models.Model):
    name = models.CharField(max_length=30)

    def get_absolute_url(self):
        return u'/post/%d' % self.id