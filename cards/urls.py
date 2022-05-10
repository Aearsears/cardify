from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='cards-index'),
    path('qa', csrf_exempt(views.qa), name='cards-qa'),
    path('qareceive', csrf_exempt(views.qareceive), name='cards-qareceive'),
]
