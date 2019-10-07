from django.urls import path
from . import views

urlpatterns = [
    path('api/nifi/', views.NifiInstanceListCreate.as_view()),
    path('api/nifi/<int:nifi_instance_id>/', views.NifiInstanceDetail.as_view()),
]
