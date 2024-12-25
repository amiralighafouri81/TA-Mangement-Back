from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
        (ADMIN, 'Administrator'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ADMIN,
    )

    def save(self, *args, **kwargs):
        # Automatically set is_staff to True if the role is 'admin'
        if self.role == self.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False

        # Call the original save method
        super().save(*args, **kwargs)
