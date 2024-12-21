from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student, Instructor
from core.models import User  # Import your custom User model

class FacultyAPITestCase(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(first_name="ali", last_name="alavi", username="alialavi", password="1234", role=User.STUDENT)
        self.user2 = User.objects.create_user(first_name="naghi", last_name="naghavi", username="naghinaghavi", password="1234", role=User.STUDENT)
        self.user3 = User.objects.create_user(first_name="ramak", last_name="ghavami", username="ramak", password="1234", role=User.INSTRUCTOR)
        self.user4 = User.objects.create_user(first_name="farshad", last_name="safaee", username="farshad", password="1234", role=User.INSTRUCTOR)

        # Create test data for students and instructors
        self.student1 = Student.objects.create(user=self.user1, student_number="1", biography="A hardworking student")
        self.student2 = Student.objects.create(user=self.user2, student_number="2", biography="A nice person")

        self.instructor1 = Instructor.objects.create(user=self.user3, staff_id="1", way_of_communication="Email", research_fields="Algorithms")
        self.instructor2 = Instructor.objects.create(user=self.user4, staff_id="2", way_of_communication="Phone", research_fields="Graph Theory")

    # Test student list endpoint
    def test_student_list(self):
        url = reverse('student-list')  # Endpoint for listing students
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    # Test student detail endpoint
    def test_student_detail(self):
        url = reverse('student-detail', args=[self.student1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['biography'], self.student1.biography)

    def test_student_detail_not_found(self):
        url = reverse('student-detail', args=[999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test instructor list endpoint
    def test_instructor_list(self):
        url = reverse('instructor-list')  # Endpoint for listing instructors
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    # Test instructor detail endpoint
    def test_instructor_detail(self):
        url = reverse('instructor-detail', args=[self.instructor1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['research_fields'], self.instructor1.research_fields)

    def test_instructor_detail_not_found(self):
        url = reverse('instructor-detail', args=[999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test student creation endpoint
    def test_create_student(self):
        url = reverse('student-list')
        data = {
            "user": {
                "first_name": "new",
                "last_name": "student",
                "username": "newstudent",
                "password": "1234",
                "role": User.STUDENT
            },
            "student_number": "3",
            "biography": "A new student"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 3)

    # Test instructor creation endpoint
    def test_create_instructor(self):
        url = reverse('instructor-list')
        data = {
            "user": {
                "first_name": "new",
                "last_name": "instructor",
                "username": "newinstructor",
                "password": "1234",
                "role": User.INSTRUCTOR
            },
            "staff_id": "3",
            "way_of_communication": "Video Call",
            "research_fields": "Machine Learning"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Instructor.objects.count(), 3)
