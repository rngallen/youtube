from django.contrib import admin
from .models import HttpError, ExceptionError, SuccessRequest

# Register your models here.


@admin.register(HttpError)
class HttpErrorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'error_message', 'timestamp']


@admin.register(ExceptionError)
class ExceptionErrorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'error_message', 'timestamp']


@admin.register(SuccessRequest)
class SuccessRequestAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'success_message', 'timestamp','search']
