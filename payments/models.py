from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Payment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.FloatField()
    externalTax = models.FloatField(null=True, blank=True)
    observation = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def calculateExternalTax(self,publishDate=timezone.now()):
        self.externalTax = self.value * 0.05

    def __str__(self):
        return self.title

class Accounts(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=80)

    def __unicode__(self):
        return self.username