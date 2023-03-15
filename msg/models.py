from django.db import models

from accounts.models import CustomUser as User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.body[:160]


class Files(models.Model):
    file = models.FileField()
    type_name = models.CharField(max_length=64)
    max_size_kbytes = models.IntegerField(default=5120)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.type_name