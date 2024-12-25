from django.db import models
from django.db.models import OneToOneField
from faculty.models import Instructor
from django.core.exceptions import ValidationError

class Course(models.Model):
    semester = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    head_TA = OneToOneField('request.Request', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    condition = models.TextField(null = True, blank=True)

    def clean(self):
        # Check if the selected head_TA (Request) is valid
        if self.head_TA:
            if not self.head_TA.student:
                raise ValidationError("The selected head_TA must be associated with a student.")

            if self.head_TA.course != self:
                raise ValidationError("The selected head_TA must have a request for this course.")

    def save(self, *args, **kwargs):
        # Validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id} - {self.name} - {self.instructor} - Semester: {self.semester} "

