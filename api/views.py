# api/views.py

from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view  # new
from rest_framework.response import Response    # new
from rest_framework.reverse import reverse      # new
from .models import Registration
from .serializers import RegistrationSerializer
from rest_framework import filters
import django_filters.rest_framework


# Create your views here.


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationDetailSearch(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    search_fields = ('plate',)
    filter_fields = ('plate', 'owner')


class RegistrationDetailFind(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    lookup_url_kwarg = 'plate'

    def get_object(self):
        return Registration.objects.get(plate=self.kwargs['plate'])

    # def get_queryset(self):
    #     return Registration.objects.get(plate=self.kwargs['plate'])


@api_view(['GET']) # new
def api_root(request, format=None):
    return Response({
        'registrations': reverse('registration-list', request=request, format=format),
        'registrations-search': reverse('registration-detail-search', request=request, format=format),
    })
