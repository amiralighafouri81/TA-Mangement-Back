from django.db import models
from faculty.models import Student



class Request(models.Model):
    REQUSET_STATUS_PENDING = 'pending'
    REQUSET_STATUS_ACCEPTED = 'accepted'
    REQUSET_STATUS_DECLINED = 'declined'
    PAYMENT_STATUS_CHOICES = [
        (REQUSET_STATUS_PENDING, 'Pending'),
        (REQUSET_STATUS_ACCEPTED, 'Accepted'),
        (REQUSET_STATUS_DECLINED, 'Declined')
    ]
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=REQUSET_STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()

    def save(self, *args, **kwargs):
        from course.models import Course
        # Check if the status is being changed to 'declined'
        if self.pk:  # Only check for existing instances
            previous = Request.objects.get(pk=self.pk)
            if previous.status == self.REQUSET_STATUS_ACCEPTED and (self.status == self.REQUSET_STATUS_DECLINED or self.status == self.REQUSET_STATUS_PENDING):
                # Check if this request is currently assigned as head_TA
                course = Course.objects.filter(head_TA=self).first()
                if course:
                    course.head_TA = None
                    course.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}"