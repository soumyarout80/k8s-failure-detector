from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Account(models.Model):
    STATE_CHOICES = (
        ("Enable", "Enable"),
        ("Disable", "Disable"),
    )
    aws_account = models.CharField(max_length=200)
    cluster_name = models.CharField(max_length=200)
    email_id = models.CharField(max_length=200)
    slack_channel = models.CharField(max_length=200, default="NA")
    notification_state = models.CharField(max_length=7,
                                          default='Enable',
                                          choices=STATE_CHOICES
                                          )
    k8s_endpoint = models.CharField(max_length=1000)

    # def __str__(self):
    #     return f"{self.aws_account} {self.cluster_name} {self.cluster_name}"


class Resource(models.Model):
    STATUS_CHOICES = (
        ("True", "True"),
        ("False", "False"),
    )
    STATE_CHOICES = (
        ("Enable", "Enable"),
        ("Disable", "Disable"),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    aws_account = models.CharField(max_length=200)
    cluster_name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    metrics = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=200)
    resource_name = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True, editable=True)
    status = models.CharField(max_length=5, default=False, choices=STATUS_CHOICES)
    status_message = models.CharField(max_length=500)
    notification_state = models.CharField(max_length=7,
                                          default='Enable',
                                          choices=STATE_CHOICES
                                          )

    class Meta:
        verbose_name_plural = "resources"

    def __str__(self):
        return f"{self.account} {self.cluster_name} {self.resource_type} {self.resource_name}"


class Alert(models.Model):
    STATUS_CHOICES = (
        ("True", "True"),
        ("False", "False"),
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    aws_account = models.CharField(max_length=200)
    cluster_name = models.CharField(max_length=200)
    metrics = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=200)
    resource_name = models.CharField(max_length=200)
    alert_status = models.CharField(max_length=5, default=False, choices=STATUS_CHOICES)
    limit = models.IntegerField(default=5)
    last_sent = models.DateTimeField()
    next_schedule = models.DateTimeField(default=timezone.now() + timedelta(minutes=30))
    count = models.IntegerField(default=0)

    def __str__(self):
        alert_resource_type = Resource().resource_type
        alert_resource_name = Resource().resource_name
        return f"{self.account} {self.cluster_name} {alert_resource_type} {alert_resource_name} "

    # def save(self, *args, **kwargs):
    #     """ On save, update timestamps """
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.modified = timezone.now()+timedelta(minutes=30)
    #     return super(User, self).save(*args, **kwargs)


class User(models.Model):
    pass
