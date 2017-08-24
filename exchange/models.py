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
    avatar = models.ImageField(upload_to='', null=True, default="default.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Wallets(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

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
    email = models.EmailField(max_length=200, default="null")
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     unique_together = ("friend", "wallet")
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Transactions(models.Model):
    walletFrom = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name='walletFrom')
    walletTo = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name='walletTo')
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    description = models.CharField(max_length=250, default="null")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(self.walletFrom, self.walletTo)




