from django.db import models


class Policy(models.Model):
    key = models.CharField(max_length=50)
    value = models.IntegerField()

    def clean(self):
        return

    def save(self, *args, **kwargs):
        # Validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id} - {self.key} : {self.value}"
