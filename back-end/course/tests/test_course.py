from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from faculty.models import Instructor, Student
from course.models import Course

@pytest.mark.django_db
class TestCreateRequest:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/course/courses/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_student_and_put_a_course_returns_403(self):
        user = get_user_model()

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
            id = 1,
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create a student user
        student_user = user.objects.create_user(
            username="student_user", password="password123", role=user.STUDENT
        )

        student = Student.objects.create(
            user = student_user,
            id = 1,
            student_number = 1223,
            biography = "hardworking"
        )

        client = APIClient()
        client.force_authenticate(user = student_user)
        response = client.put('/course/courses/1/', {"head_TA" : 1})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_instructor_and_put_condition_returns_200(self):
        # Get the custom User model
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
            id = 1,
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Authenticate the student user
        client = APIClient()
        client.force_authenticate(user=instructor_user)

        # Make the POST request to create a request
        response = client.put('/course/courses/1/', {"condition": 18})

        course.refresh_from_db()

        # Assert the response status code
        assert response.status_code == status.HTTP_200_OK and course.condition == 18