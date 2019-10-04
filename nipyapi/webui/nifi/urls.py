from django.urls import path
from . import views

urlpatterns = [
    path('api/nifi/', views.NifiInstanceListCreate.as_view()),
]
