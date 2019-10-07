from django.db import models


class NifiInstance(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='PENDING_CREATE')
    created_at = models.DateTimeField(auto_now_add=True)
