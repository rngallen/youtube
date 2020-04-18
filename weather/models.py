from django.db import models

# Create your models here.


class City(models.Model):
    city_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CITY'
        managed = True
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['-timestamp']

    # def get_absolute_url(self):
    #     return reverse("detail", kwargs={"pk": self.pk})

