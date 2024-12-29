from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Course
from request.models import Request

@receiver(pre_save, sender=Course)
def handle_condition_change(sender, instance, **kwargs):
    # Check if the course condition is being updated and if it's different from the original
    if instance.pk:  # If the course already exists
        old_course = Course.objects.get(pk=instance.pk)
        if old_course.condition != instance.condition:  # Condition has changed
            # Find requests where the student's score no longer meets the new condition
            requests_to_decline = Request.objects.filter(course=instance, status=Request.REQUSET_STATUS_ACCEPTED)
            for request in requests_to_decline:
                if request.score < instance.condition:
                    request.status = Request.REQUSET_STATUS_DECLINED
                    request.save()

                    # If the student was the head TA, remove them as head TA
                    if instance.head_TA and instance.head_TA.student == request.student:
                        instance.head_TA = None
                        instance.save()