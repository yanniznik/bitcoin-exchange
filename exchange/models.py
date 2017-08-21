import random
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    zip = models.IntegerField(null=True, default="00000")
    country = models.CharField(max_length=50, null=True)
    avatar = models.ImageField('avatar', upload_to='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wallets(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallets.objects.create(owner=instance, address = uuid.uuid4().hex)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Contacts(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wallet = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)



class Transactions(models.Model):
    walletFrom = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    walletTo = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)




