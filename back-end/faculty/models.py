from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import User

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_number = models.CharField(error_messages={'unique': 'A student with that student number already exists.'},
                                      max_length=10, unique=True)
    # resume_link
    biography = models.TextField()

    def clean(self):
        # Check if the user's role is "student"
        if self.user.role != User.STUDENT:
            raise ValidationError("User must have a 'Student' role to be added as a Student.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    class Meta:
        ordering = ["id"]

class Instructor(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.CharField(error_messages={'unique': 'An instructor with that staff id already exists.'},
                                max_length=10, unique=True)
    way_of_communication = models.TextField()
    research_fields = models.TextField()

    def clean(self):
        # Check if the user's role is "instructor"
        if self.user.role != User.INSTRUCTOR:
            raise ValidationError("User must have an 'Instructor' role to be added as an Instructor.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    class Meta:
        ordering = ["id"]