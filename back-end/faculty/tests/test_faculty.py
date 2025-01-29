from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from faculty.models import Instructor, Student


@pytest.mark.django_db
class TestFaculty:
    def test_if_user_is_student_and_get_instructors_list_returns_200(self):
        # Get the User model
        User = get_user_model()

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
            biography="Test student"
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Make GET request to instructors endpoint
        response = client.get('/faculty/instructors/')

        # Assert response status code is 200
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_student_and_get_students_list_returns_200(self):
        # Get the User model
        User = get_user_model()

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
            biography="Test student"
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Make GET request to students endpoint
        response = client.get('/faculty/students/')

        # Assert response status code is 403
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_instructor_and_get_instructors_list_returns_200(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        Instructor.objects.create(
            user=instructor_user,
            staff_id="INST123",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create API client and authenticate as instructor
        client = APIClient()
        client.force_authenticate(user=instructor_user)

        # Make GET request to instructors endpoint
        response = client.get('/faculty/instructors/')

        # Assert response status code is 200
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_instructor_and_get_students_list_returns_200(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        Instructor.objects.create(
            user=instructor_user,
            staff_id="INST123",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create API client and authenticate as instructor
        client = APIClient()
        client.force_authenticate(user=instructor_user)

        # Make GET request to students endpoint
        response = client.get('/faculty/students/')

        # Assert response status code is 403
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_student_and_post_instructor_returns_403(self):
        # Get the User model
        User = get_user_model()

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
            biography="Test student"
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Prepare instructor data
        instructor_data = {
            "staff_id": "INST123",
            "way_of_communication": "Email",
            "research_fields": "Computer Science"
        }

        # Make POST request to instructors endpoint
        response = client.post('/faculty/instructors/', instructor_data)

        # Assert response status code is 403
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You do not have permission to update this object." in str(response.data['detail'])

    def test_if_user_is_student_and_put_instructor_returns_403(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user for the record to update
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id="INST123",
            way_of_communication="Email",
            research_fields="Computer Science"
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
            biography="Test student"
        )

        # Create API client and authenticate as student
        client = APIClient()
        client.force_authenticate(user=student_user)

        # Prepare update data
        update_data = {
            "way_of_communication": "Slack",
            "research_fields": "AI"
        }

        # Make PUT request to instructors endpoint
        response = client.put(f'/faculty/instructors/{instructor.id}/', update_data)

        # Assert response status code is 403
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You do not have permission to update this object." in str(response.data['detail'])

    def test_if_user_is_instructor_and_post_instructor_returns_403(self):
        # Get the User model
        User = get_user_model()

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username="instructor_user",
            password="password123",
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        Instructor.objects.create(
            user=instructor_user,
            staff_id="INST123",
            way_of_communication="Email",
            research_fields="Computer Science"
        )

        # Create API client and authenticate as instructor
        client = APIClient()
        client.force_authenticate(user=instructor_user)

        # Prepare instructor data
        instructor_data = {
            "staff_id": "INST456",
            "way_of_communication": "Slack",
            "research_fields": "AI"
        }

        # Make POST request to instructors endpoint
        response = client.post('/faculty/instructors/', instructor_data)

        # Assert response status code is 403
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You do not have permission to update this object." in str(response.data['detail'])