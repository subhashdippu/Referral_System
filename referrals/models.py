from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=20, null=True, blank=True)
    registration_timestamp = models.DateTimeField(auto_now_add=True)


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(
        User, related_name='referred_by', on_delete=models.CASCADE)
    registration_timestamp = models.DateTimeField(auto_now_add=True)
