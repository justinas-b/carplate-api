# api/urls.py

from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('api/', views.RegistrationList.as_view(), name='registration-list'),
    path('api/<int:pk>/', views.RegistrationDetail.as_view(), name='registration-detail'),
    path('api', views.RegistrationDetailSearch.as_view(), name='registration-detail-search'),
    re_path(r'^api/plate/(?P<plate>.*)/$', views.RegistrationDetailFind.as_view(), name='registration-detail-find'),
    re_path(r'^docs/', get_swagger_view(title='Car Plate API documentation'), name='api-documentation'),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
