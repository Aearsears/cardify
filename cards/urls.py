from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cards-index'),
    path('create', views.create, name='cards-create'),
]
