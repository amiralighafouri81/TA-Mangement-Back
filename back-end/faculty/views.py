from rest_framework.viewsets import ModelViewSet
from .models import Student, Instructor
from .serializers import StudentSerializer, InstructorSerializer

# @api_view()
# def student_list(request):
#     queryset = Student.objects.all()
#     serializer = StudentSerializer(queryset, many=True)
#     return Response(serializer.data)
#
# @api_view()
# def student_detail(request, id):
#     student = get_object_or_404(Student, pk=id)
#     serializer = StudentSerializer(student)
#     return Response(serializer.data)
#
#
# @api_view()
# def instructor_list(request):
#     queryset = Instructor.objects.all()
#     serializer = InstructorSerializer(queryset, many=True)
#     return Response(serializer.data)
#
# @api_view()
# def instructor_detail(request, id):
#     instructor = get_object_or_404(Instructor, pk=id)
#     serializer = InstructorSerializer(instructor)
#     return Response(serializer.data)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_serializer_context(self):
        return {'request': self.request}
