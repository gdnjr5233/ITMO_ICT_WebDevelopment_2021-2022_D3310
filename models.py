from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True, unique=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    salary = models.IntegerField(default=0)
    cell = models.ManyToManyField('Cell', through="Service")


    REQUIRED_FIELDS = ['first_name', 'last_name', 'passport']

    def __str__(self):
        return self.username

class Chicken(models.Model):
    breed = models.ForeignKey('Breed', on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    egg_amount = models.IntegerField(default=0)
    cell = models.ForeignKey('Cell', on_delete=models.CASCADE)

class Breed(models.Model):
    PROD = (
      ("low", "low"),
      ("avg", "average"),
      ("high", "high")
    )
    breed = models.CharField(max_length=50)
    productivity = models.CharField(max_length=4, choices=PROD)
    avg_weight = models.IntegerField(default=0)
    diet = models.TextField()

    def __str__(self):
        return self.breed

class Cell(models.Model):
    cell = models.IntegerField(default=0)
    row = models.ForeignKey('Row', on_delete=models.CASCADE)
    tsekh = models.ForeignKey('Tsekh', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cell)

class Row(models.Model):
    row = models.IntegerField(default=0)
    tsekh = models.ForeignKey('Tsekh', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.row)

class Tsekh(models.Model):
    tsekh = models.IntegerField(default=0)

    def __str__(self):
        return str(self.tsekh)

class Service(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    cell = models.ForeignKey('Cell', on_delete=models.CASCADE)
    status = models.BooleanField(blank=True, null=True)
