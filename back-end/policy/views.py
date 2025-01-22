from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Policy
from .pagination import DefaultPagination
from .serializers import StudentPolicySerializer, InstructorPolicySerializer, AdminPolicySerializer


class PolicyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    pagination_class = DefaultPagination

    def get_serializer_class(self):
        # Get the user role and return the corresponding serializer
        user = self.request.user
        if user.role == 'instructor':
            return InstructorPolicySerializer
        elif user.role == 'student':
            return StudentPolicySerializer
        elif user.role =='admin':
            return AdminPolicySerializer

    def get_queryset(self):
        return Policy.objects.all().values()

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'admin':
            raise PermissionDenied("You do not have permission to update this object.")

        return super().update(request, *args, **kwargs)

