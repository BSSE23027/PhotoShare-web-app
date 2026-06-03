from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Users(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, default="")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Images(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')
    created_at = models.DateTimeField(auto_now_add=True)  # Add this



# Create your models here.
