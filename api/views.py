# api/views.py

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('plate',)
    filter_fields = ('plate', 'owner')


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Retrieve car plate registration details

    patch:
        Update existing car plate registration details

    delete:
        Delete existing car plate registration details

    put:
        Create new car plate registration

    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationDetailFind(generics.RetrieveUpdateDestroyAPIView):

    """View for Registration Details where plate is passed as argument in URL.

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
def api_root(request):
    """List available API endpoints."""
    return Response({
        'registrations': reverse('registration-list', request=request),
    })
