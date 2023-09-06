from django.urls import path
from . import views


urlpatterns = [
    path('getImages/', views.getImages, name='get'),
]