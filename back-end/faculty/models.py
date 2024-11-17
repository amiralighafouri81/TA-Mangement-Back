from django.db import models
from django.conf import settings

class Student(models.Model):
    ENTRANCE_YEAR_1399 = 1399
    ENTRANCE_YEAR_1400 = 1400
    ENTRANCE_YEAR_1401 = 1401
    ENTRANCE_YEAR_1402 = 1402
    ENTRANCE_YEAR_1403 = 1403
    ENTRANCE_YEAR_CHOICES = [
        (ENTRANCE_YEAR_1399, 1399),
        (ENTRANCE_YEAR_1400, 1400),
        (ENTRANCE_YEAR_1401, 1401),
        (ENTRANCE_YEAR_1402, 1402),
        (ENTRANCE_YEAR_1403, 1403)
    ]
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField()
    entrance_year = models.IntegerField(choices=ENTRANCE_YEAR_CHOICES, default=ENTRANCE_YEAR_1400)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ["id"]

class Instructor(models.Model):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ["id"]