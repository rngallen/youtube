from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Entry(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entry # {self.id}"

    class Meta:
        db_table = "ENTRY"
        managed = True
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
        ordering = ["-timestamp"]

    # def get_absolute_url(self):
    #     return reverse("detail", kwargs={"pk": self.pk})
