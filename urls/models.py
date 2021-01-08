from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from logic.models import Project as EthereumProject


class Project(models.Model):
    project = models.ForeignKey(EthereumProject, on_delete=models.CASCADE, related_name='details', related_query_name='details')
    public_id = models.UUIDField()
    max_requests_per_month = models.PositiveIntegerField(null=True, blank=True, default=None)
    max_requests_per_second = models.PositiveIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.public_id}"

    class Meta:
        db_table = "project_ids"


class AllowedAddress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    address = models.CharField(max_length=42)

    def __str__(self):
        return f"{self.address}"

    class Meta:
        db_table = "allowed_addresses"
        unique_together = ("project", "address", )


class AllowedClient(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(default=None, blank=True, null=True)

    def __str__(self):
        return self.ip

    class Meta:
        db_table = "allowed_clients"
        unique_together = ("project", "ip", )
