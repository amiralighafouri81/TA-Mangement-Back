from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import User
import os


def student_directory_path(student, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}_{1}_{2}/{3}'.format(student.user.id, student.id, student.student_number, filename)


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_number = models.CharField(error_messages={'unique': 'A student with that student number already exists.'},
                                      max_length=10, unique=True)
    resume_file = models.FileField(blank=True, upload_to=student_directory_path, max_length=200)
    biography = models.TextField()

    def clean(self):
        # Check if the user's role is "student"
        if self.user.role != User.STUDENT:
            raise ValidationError("User must have a 'Student' role to be added as a Student.")
        if not (self.resume_file.name is None or self.resume_file.name == "" or self.resume_file.name.endswith('.pdf')):
            raise ValidationError("type of file must be pdf {0}".format(self.resume_file.name))
        if self.resume_file.name is not None and self.resume_file.name != "" and self.resume_file.size > 1024 * 1024:
            raise ValidationError("maximum size of file is 1MB.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving

        obj = Student.objects.filter(id=self.id).first()
        old_resume_file = None
        if obj is not None:
            old_resume_file = obj.resume_file
        if old_resume_file is not None and old_resume_file.name is not None and old_resume_file.name != "":
            _delete_file(old_resume_file.path)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        resume_file = self.resume_file
        if resume_file.name is not None and resume_file.name != "":
            _delete_file(resume_file.path)
        super().delete(using, keep_parents)

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
