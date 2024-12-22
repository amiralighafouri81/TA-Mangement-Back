from django.db import models
from django.db.models import OneToOneField
from faculty.models import Instructor

class Course(models.Model):
    semester = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    head_TA = OneToOneField('request.Request', on_delete=models.SET_NULL, null=True, related_name='+')
    condition = models.TextField(null = True)

