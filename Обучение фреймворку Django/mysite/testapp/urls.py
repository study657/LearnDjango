from django.urls import path
from .views import *

urlpatterns = [
    path('', test, name='test')
]