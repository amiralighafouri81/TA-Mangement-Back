from django.db import models
from faculty.models import Instructor
from rest_framework.exceptions import PermissionDenied
from request.models import Request


class Course(models.Model):
    semester = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    head_TA = models.OneToOneField(
        'request.Request',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    condition = models.FloatField(null=True, blank=True)
    max_TA_number = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        # Check if the selected head_TA is valid
        if self.head_TA:
            if not self.head_TA.student:
                raise PermissionDenied("The selected head_TA must be associated with a student.")
            if self.head_TA.course != self:
                raise PermissionDenied("The selected head_TA must have a request for this course.")
            if self.head_TA.status != Request.REQUSET_STATUS_ACCEPTED:
                raise PermissionDenied("The selected head_TA must have an accepted request.")

        if self.condition is not None:
            if self.instructor and (self.condition < 10 or self.condition > 20):
                raise PermissionDenied("condition must be between 10 and 20.")

    def save(self, *args, **kwargs):
        # Validate before saving
        self.clean()
        super().save(*args, **kwargs)



    def __str__(self):
        return f"id: {self.id} - {self.name} - {self.instructor} - Semester: {self.semester} "


