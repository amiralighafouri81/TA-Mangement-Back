from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from faculty.models import Instructor
from course.models import Course
from request.models import Request
from faculty.models import Student

@pytest.mark.django_db
class TestRequest:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/request/requests/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_instructor_and_post_a_request_returns_403(self):
        user = get_user_model()
        instructor_user = user.objects.create_user(
            username="instructor_user", password="password123", role=user.INSTRUCTOR
        )

        client = APIClient()
        client.force_authenticate(user = {})
        response = client.post('/request/requests/', {"status": "pending"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_student_and_score_satisfies_condition_returns_201(self):
        user = get_user_model()

        # Create an instructor user
        instructor_user = user.objects.create_user(
            username="instructor_user", password="password123", role=user.INSTRUCTOR
        )
        # Create an instructor instance
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id="INSTR001",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create a course and assign it to the instructor
        course = Course.objects.create(
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create a student user
        student_user = user.objects.create_user(
            username="student_user", password="password123", role=user.STUDENT
        )

        # Authenticate the student user
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Make the POST request to create a request
        response = client.post('/request/requests/', {"course_id": course.id, "score": 19})

        # Assert the response status code
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_student_and_score_below_condition_returns_403(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id="INSTR001",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create a course with condition 17.0
        course = Course.objects.create(
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create a student user
        student_user = User.objects.create_user(
            username="student_user",
            password="password123",
            role=User.STUDENT
        )

        # Create student profile
        Student.objects.create(
            user=student_user,
            student_number="12345",
            biography="hardworking"
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Try to create request with score below condition
        response = client.post('/request/requests/', {
            "course_id": course.id,
            "score": 16.0  # Below course condition of 17.0
        })

        # Assert response status code is 403
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Verify error message
        assert "Your request is declined because your score (16.0) is lower than the required score for this course." in str(
            response.data['detail'])

        # Verify request was created with declined status
        request = Request.objects.first()
        assert request is not None
        assert request.status == Request.REQUSET_STATUS_DECLINED

    def test_if_user_is_student_and_delete_pending_request_returns_204(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id="INSTR001",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create a course
        course = Course.objects.create(
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create a student user
        student_user = User.objects.create_user(
            username="student_user",
            password="password123",
            role=User.STUDENT
        )

        # Create student profile
        student = Student.objects.create(
            user=student_user,
            student_number="12345",
            biography="hardworking"
        )

        # Create a pending request
        request = Request.objects.create(
            course=course,
            student=student,
            status=Request.REQUSET_STATUS_PENDING,
            score=18.0
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Try to delete the pending request
        response = client.delete(f'/request/requests/{request.id}/')

        # Assert response status code is 204 (No Content)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify request was deleted from database
        assert not Request.objects.filter(id=request.id).exists()

    def test_if_user_is_student_and_delete_declined_or_accepted_request_returns_403(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id="INSTR001",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create a course
        course = Course.objects.create(
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create a student user
        student_user = User.objects.create_user(
            username="student_user",
            password="password123",
            role=User.STUDENT
        )

        # Create student profile
        student = Student.objects.create(
            user=student_user,
            student_number="12345",
            biography="hardworking"
        )

        # Create an accepted request
        accepted_request = Request.objects.create(
            course=course,
            student=student,
            status=Request.REQUSET_STATUS_ACCEPTED,
            score=18.0
        )

        # Create a declined request
        declined_request = Request.objects.create(
            course=course,
            student=student,
            status=Request.REQUSET_STATUS_DECLINED,
            score=16.0
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Try to delete the accepted request
        response = client.delete(f'/request/requests/{accepted_request.id}/')

        # Assert response status code is 403 for accepted request
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Students are not allowed to delete a request with accepted or declined status." in str(
            response.data['detail'])

        # Verify accepted request still exists in database
        assert Request.objects.filter(id=accepted_request.id).exists()

        # Try to delete the declined request
        response = client.delete(f'/request/requests/{declined_request.id}/')

        # Assert response status code is 403 for declined request
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Students are not allowed to delete a request with accepted or declined status." in str(
            response.data['detail'])

        # Verify declined request still exists in database
        assert Request.objects.filter(id=declined_request.id).exists()
