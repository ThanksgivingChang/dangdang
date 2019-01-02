from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=10)
    status = models.BooleanField()
    class Meta:
        db_table='d_user'