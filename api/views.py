# api/views.py

import django_filters.rest_framework
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from .models import Registration
from .serializers import RegistrationSerializer


# Create your views here.


class RegistrationList(generics.ListCreateAPIView):
    """
    get:
        List all existing or create new car plate registration

    post:
        Create new car plate registration.

    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        # retrieve_image.delay(plate=request.data["plate"])
        # debug_task.delay()
        return super().post(request, *args, **kwargs)


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Retrieve car plate registration details

    update:
        Update existing car plate registration details

    delete:
        Delete existing car plate registration details
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationDetailSearch(generics.ListCreateAPIView):
    """
    get:
        List existing car plate registrations. Supports search and filtering.

    post:
        Create new car plate registration.
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    search_fields = ('plate',)
    filter_fields = ('plate', 'owner')


class RegistrationDetailFind(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Retrieve car plate registration details

    update:
        Update existing car plate registration details

    delete:
        Delete existing car plate registration details
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    lookup_url_kwarg = 'plate'

    def get_object(self):
        return Registration.objects.get(plate=self.kwargs['plate'])

    # def get_queryset(self):
    #     return Registration.objects.get(plate=self.kwargs['plate'])


@api_view(['GET'])
def api_root(request, format=None):
    """Lists available API endpoints"""

    return Response({
        'registrations': reverse('registration-list', request=request, format=format),
        'registrations-search': reverse('registration-detail-search', request=request, format=format),
        'api-documentation': '',  # TODO: Add link to documentation
        'admin': '',  # TODO: Add link to documentation
    })
