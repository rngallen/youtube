from django.db import models

# Create your models here.





class HttpError(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    error_message = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField(
        protocol="both", unpack_ipv4=False)

    def __str__(self):
        return self.ip_address


class ExceptionError(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    error_message = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField(
        protocol="both", unpack_ipv4=False)

    def __str__(self):
        return self.ip_address

class SuccessRequest(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    success_message = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    search = models.CharField(max_length=200)

    def __str__(self):
        return self.ip_address
    