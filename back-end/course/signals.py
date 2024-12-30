from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Course
from request.models import Request

@receiver(pre_save, sender=Course)
def handle_condition_change(sender, instance, **kwargs):
    # Check if the course already exists in the database
    if instance.pk:  # If the course already exists
        try:
            old_course = Course.objects.get(pk=instance.pk)
            # Check if the condition has changed
            if old_course.condition != instance.condition:
                # Find requests where the student's score no longer meets the new condition
                requests_to_decline = Request.objects.filter(
                    course=instance,
                    status=Request.REQUSET_STATUS_ACCEPTED
                )
                for request in requests_to_decline:
                    if request.score < instance.condition:
                        # Update the request status to declined
                        request.status = Request.REQUSET_STATUS_DECLINED
                        request.save()

                        # Remove the student as head TA if necessary
                        if instance.head_TA and instance.head_TA.student == request.student:
                            instance.head_TA = None
                            instance.save()
        except Course.DoesNotExist:
            # This should not happen as we checked instance.pk, but it's good to handle it
            pass
