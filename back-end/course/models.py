from django.db import models
from django.db.models import OneToOneField
from faculty.models import Instructor

class Course(models.Model):
    semester = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    head_TA = OneToOneField('request.Request', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    condition = models.TextField(null = True, blank=True)

    def __str__(self):
        return f"{self.name} - Semester: {self.semester} - Instructor: {self.instructor}"

