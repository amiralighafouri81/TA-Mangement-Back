from django.db import models
from faculty.models import Student


class Request(models.Model):
    REQUSET_STATUS_PENDING = 'pending'
    REQUSET_STATUS_COMPLETE = 'complete'
    REQUSET_STATUS_FAILED = 'failed'
    PAYMENT_STATUS_CHOICES = [
        (REQUSET_STATUS_PENDING, 'Pending'),
        (REQUSET_STATUS_COMPLETE, 'Complete'),
        (REQUSET_STATUS_FAILED, 'Failed')
    ]
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=REQUSET_STATUS_PENDING)
    date = models.DateField(auto_now_add=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student}"