from django.contrib import admin
from .models import City

# Register your models here.


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["city_id", "name", "country", "timestamp"]
