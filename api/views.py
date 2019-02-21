# api/views.py

from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .forms import RegistrationForm
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


class AppList(APIView):

    def get(self, request):
        queryset = Registration.objects.all()
        if queryset:
            response = render_to_response('registration_list.html', {'registrations': queryset})
        else:
            response = render(request=request, template_name='registration_list.html')

        return response


class AppDetails(APIView):

    def get(self, request, pk):
        form = RegistrationForm(instance=Registration.objects.get(pk=pk))
        return render(request=request, template_name="registration_details.html", context={'form': form})

    def post(self, request, pk):
        form = RegistrationForm(request.POST or None, instance=Registration.objects.get(pk=pk))

        if 'cancel' in request.POST:
            print("form has been canceled")
            response = redirect('app-list')
        elif form.is_valid():
            post = form.save(commit=False)
            post.save()
            response = redirect('app-list')
        else:
            response = render(request=request, template_name="registration_details.html",
                              context={'form': form, 'error': form.errors})

        return response


class AppCreate(APIView):

    def get(self, request):
        form = RegistrationForm()
        return render(request=request, template_name="registration_details.html", context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            response = redirect('app-list')
        else:
            response = render(request=request, template_name="registration_details.html",
                              context={'form': form, 'error': form.errors})

        return response


class AppDelete(APIView):

    def delete_record(self, pk):
        registration = get_object_or_404(Registration, pk=pk)
        registration.delete()

    def get(self, request, pk):
        self.delete_record(pk=pk)
        return redirect(to='app-list')


@api_view(['GET'])
def api_root(request):
    """List available API endpoints."""
    return Response({
        'app': reverse('app-list', request=request),
        'api': reverse('registration-list', request=request),

    })
