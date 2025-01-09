from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from faculty.models import Instructor, Student
from course.models import Course
from course.models import Request

@pytest.mark.django_db
class TestCourse:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/course/courses/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_student_or_instructor_post_course_returns_403(self):
        # Get the User model
        User = get_user_model()

        # Create a student user
        student_user = User.objects.create_user(
            username='student',
            password='testpass123',
            first_name='Test',
            last_name='Student',
            role=User.STUDENT
        )

        # Create student profile
        Student.objects.create(
            user=student_user,
            student_number='12345',
            biography='Test biography'
        )

        # Create an instructor user
        instructor_user = User.objects.create_user(
            username='instructor',
            password='testpass123',
            first_name='Test',
            last_name='Instructor',
            role=User.INSTRUCTOR
        )

        # Create instructor profile
        instructor = Instructor.objects.create(
            user=instructor_user,
            staff_id='INST123',
            way_of_communication='Email',
            research_fields='Computer Science'
        )

        # Prepare course data
        course_data = {
            'name': 'Test Course',
            'semester': 'Fall 2024',
            'instructor': instructor.id,
            'condition': 15.0
        }

        # Test with student user
        client = APIClient()
        client.force_authenticate(user=student_user)
        response = client.post('/course/courses/', course_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test with instructor user
        client.force_authenticate(user=instructor_user)
        response = client.post('/course/courses/', course_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Verify no course was created
        assert Course.objects.count() == 0

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

    def test_if_user_is_instructor_and_put_headTA_returns_200(self):
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

        # Create a course
        course = Course.objects.create(
            semester="Fall 2024",
            instructor=instructor,
            name="Introduction to Programming",
            condition=17.0
        )

        # Create an accepted request for the student
        request = Request.objects.create(
            course=course,
            student=student,
            status=Request.REQUSET_STATUS_ACCEPTED,
            score=18.0
        )

        # Create API client and authenticate as instructor
        client = APIClient()
        client.force_authenticate(user=instructor_user)

        # Make PUT request to update head_TA
        response = client.put(f'/course/courses/{course.id}/', {
            'head_TA': request.id
        })

        # Refresh course from database
        course.refresh_from_db()

        # Assert response status code is 200 and head_TA was set correctly
        assert response.status_code == status.HTTP_200_OK
        assert course.head_TA_id == request.id

        # Verify response data
        assert response.data['head_TA']['id'] == student.id
        assert response.data['head_TA']['first_name'] == student_user.first_name
        assert response.data['head_TA']['last_name'] == student_user.last_name
        assert response.data['head_TA']['student_number'] == student.student_number