from django.db import models


class Hash(models.Model):
    text = models.TextField()
    sha256 = models.CharField(max_length=64)


