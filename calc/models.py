from django.db import models

# Create your models here.
class Table(models.Model):
    target = models.CharField(max_length=100, null=True)
    dist = models.CharField(max_length=100, null=True)

    first_try = models.CharField(max_length=100)
    second_try = models.CharField(max_length=100)
    third_try = models.CharField(max_length=100)

    mrad = models.CharField(max_length=100)


class TableIpAddressSort(models.Model):
    ip = models.GenericIPAddressField(null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)


    def __str__(self):
        return self.ip

