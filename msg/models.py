from django.db import models


class Messages(models.Model):
    sender = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)

    def __str__(self):
        return self.body[:160]
