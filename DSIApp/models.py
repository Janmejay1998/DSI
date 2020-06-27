from django.db import models

# Create your models here.

class log(models.Model):
    Username = models.CharField(max_length=25)
    Password = models.CharField(max_length=25)
    

class Student(models.Model):
    Name = models.CharField(max_length=25)
    Age = models.IntegerField()
    Email = models.CharField(max_length=25, null=True)
    Mob = models.IntegerField()
    Add = models.CharField(max_length=64)
    Pass = models.CharField(max_length=25, null=True)
    Re_Pass = models.CharField(max_length=25, null=True)

    
