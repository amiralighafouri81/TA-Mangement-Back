from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from faculty.models import Instructor, Student
from course.models import Course

@pytest.mark.django_db
class TestCore:
    def test_if_user_registers_correctly_returns_201(self):
        client = APIClient()
        registration_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirmation': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'student_number': '12345'
        }
        test_user = get_user_model()

        # Make POST request to registration endpoint
        response = client.post('/auth/users/', registration_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert test_user.objects.filter(username='testuser').exists()
        assert Student.objects.filter(student_number='12345').exists()
        assert 'id' in response.data
        assert response.data['username'] == 'testuser'
        assert response.data['first_name'] == 'Test'
        assert response.data['last_name'] == 'User'

    def test_if_user_login_returns_200(self):
        # Get the User model
        test_user = get_user_model()

        # Create a test user
        test_user = test_user.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=test_user.STUDENT
        )

        # Create associated student profile
        Student.objects.create(
            user=test_user,
            student_number='12345',
            biography='Test biography'
        )

        # Create API client
        client = APIClient()

        # Prepare login data
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        # Make POST request to JWT token endpoint
        response = client.post('/auth/jwt/create/', login_data)

        # Assert response status code is 200 (OK)
        assert response.status_code == status.HTTP_200_OK

        # Verify response contains access and refresh tokens
        assert 'access' in response.data

        # Verify tokens are non-empty strings
        assert isinstance(response.data['access'], str)
        assert len(response.data['access']) > 0

    def test_if_student_update_profile_returns_200(self):
        # Get the User model
        User = get_user_model()

        # Create a test student user
        test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=User.STUDENT
        )

        # Create associated student profile
        Student.objects.create(
            user=test_user,
            student_number='12345',
            biography='Test biography'
        )

        # Create API client and authenticate
        client = APIClient()
        client.force_authenticate(user=test_user)

        # Prepare update data
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'biography': 'Updated biography',
            'student_number': '12345'  # Keeping the same student number
        }

        # Make PATCH request to user profile endpoint
        response = client.patch('/auth/users/me/', update_data)

        # Assert response status code is 200 (OK)
        assert response.status_code == status.HTTP_200_OK

        # Refresh user from database
        test_user.refresh_from_db()
        student = Student.objects.get(user=test_user)

        # Verify user data was updated
        assert test_user.first_name == 'Updated'
        assert test_user.last_name == 'Name'
        assert student.biography == 'Updated biography'

        # Verify response data
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
        assert response.data['biography'] == 'Updated biography'
        assert response.data['student_number'] == '12345'

    def test_if_instructor_update_profile_returns_200(self):
        # Get the User model
        User = get_user_model()

        # Create a test instructor user
        test_user = User.objects.create_user(
            username='instructor',
            password='testpass123',
            first_name='Test',
            last_name='Instructor',
            role=User.INSTRUCTOR
        )

        # Create associated instructor profile
        Instructor.objects.create(
            user=test_user,
            staff_id='INST123',
            way_of_communication='Email only',
            research_fields='Computer Science'
        )

        # Create API client and authenticate
        client = APIClient()
        client.force_authenticate(user=test_user)

        # Prepare update data
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Instructor',
            'way_of_communication': 'Email and Slack',
            'research_fields': 'Computer Science, AI',
            'staff_id': 'INST123'  # Keeping the same staff_id
        }

        # Make PATCH request to user profile endpoint
        response = client.patch('/auth/users/me/', update_data)

        # Assert response status code is 200 (OK)
        assert response.status_code == status.HTTP_200_OK

        # Refresh user from database
        test_user.refresh_from_db()
        instructor = Instructor.objects.get(user=test_user)

        # Verify user data was updated
        assert test_user.first_name == 'Updated'
        assert test_user.last_name == 'Instructor'
        assert instructor.way_of_communication == 'Email and Slack'
        assert instructor.research_fields == 'Computer Science, AI'

        # Verify response data
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Instructor'
        assert response.data['way_of_communication'] == 'Email and Slack'
        assert response.data['research_fields'] == 'Computer Science, AI'
        assert response.data['staff_id'] == 'INST123'

    def test_if_register_with_existing_username_returns_400(self):
        # Get the User model
        User = get_user_model()

        # Create a user first
        User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=User.STUDENT
        )

        # Create API client
        client = APIClient()

        # Prepare registration data with same username
        registration_data = {
            'username': 'testuser',  # Same username as existing user
            'password': 'testpass123',
            'password_confirmation': 'testpass123',
            'first_name': 'Another',
            'last_name': 'User',
            'student_number': '54321'
        }

        # Make POST request to registration endpoint
        response = client.post('/auth/users/', registration_data)

        # Assert response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Verify error message
        assert 'username' in response.data
        assert 'A user with that username already exists.' in str(response.data['username'])

    def test_if_user_update_profile_with_existing_unique_field_returns_400(self):
        # Get the User model
        User = get_user_model()

        # Create first student user
        first_user = User.objects.create_user(
            username='student1',
            password='testpass123',
            first_name='First',
            last_name='Student',
            role=User.STUDENT
        )

        # Create first student profile
        Student.objects.create(
            user=first_user,
            student_number='12345',
            biography='First student'
        )

        # Create second student user
        second_user = User.objects.create_user(
            username='student2',
            password='testpass123',
            first_name='Second',
            last_name='Student',
            role=User.STUDENT
        )

        # Create second student profile
        Student.objects.create(
            user=second_user,
            student_number='54321',
            biography='Second student'
        )

        # Create API client and authenticate as second user
        client = APIClient()
        client.force_authenticate(user=second_user)

        # Try to update with first student's student number
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'biography': 'Updated biography',
            'student_number': '12345'  # Using first student's number
        }

        # Make PATCH request to user profile endpoint
        response = client.patch('/auth/users/me/', update_data)

        # Assert response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Verify error message
        assert 'student_number' in response.data
        assert 'A student with that student number already exists.' in str(response.data['student_number'])

        # Verify database wasn't updated
        second_user.refresh_from_db()
        second_student = Student.objects.get(user=second_user)
        assert second_student.student_number == '54321'

    def test_if_password_and_password_conf_not_match_returns_400(self):
        # Create API client
        client = APIClient()

        # Prepare registration data with mismatched passwords
        registration_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirmation': 'differentpass123',  # Different from password
            'first_name': 'Test',
            'last_name': 'User',
            'student_number': '12345'
        }

        # Make POST request to registration endpoint
        response = client.post('/auth/users/', registration_data)

        # Assert response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Verify error message
        assert 'password_confirmation' in response.data
        assert 'Passwords do not match.' in str(response.data['password_confirmation'])

        # Verify user was not created in database
        User = get_user_model()
        assert not User.objects.filter(username='testuser').exists()

        # Verify student profile was not created
        assert not Student.objects.filter(student_number='12345').exists()




