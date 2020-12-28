from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Manager(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    registration_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    modification_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "managers"


class Project(models.Model):
    manager = models.ForeignKey(Manager,
                                default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.manager}"

    class Meta:
        db_table = "projects"
