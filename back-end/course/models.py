from django.db import models
from faculty.models import Instructor

class Course(models.Model):
    semester = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    # headTARef
    condition = models.TextField()

