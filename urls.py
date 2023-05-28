from django.urls import path
from . import views

urlpatterns = [
    path('', views.alerte_investigation, name='alerte_investigation'),
]
