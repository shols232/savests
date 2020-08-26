from django.db import models

class SendEmail(models.Model):
    subject = models.CharField(max_length=300)
    body = models.TextField()

