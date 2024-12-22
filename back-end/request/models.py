from django.db import models
from faculty.models import Student


class Request(models.Model):
    REQUSET_STATUS_PENDING = 'P'
    REQUSET_STATUS_COMPLETE = 'C'
    REQUSET_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (REQUSET_STATUS_PENDING, 'Pending'),
        (REQUSET_STATUS_COMPLETE, 'Complete'),
        (REQUSET_STATUS_FAILED, 'Failed')
    ]
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=REQUSET_STATUS_PENDING)
    date = models.DateField(auto_now_add=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)