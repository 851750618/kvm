from django.db import models

class User_role(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Package_review(models.Model):
    user = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=3000)
    path = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name



