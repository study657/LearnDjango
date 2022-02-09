from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('test/', test),
    path('category/<int:category_id>/', get_category), # В таких скобочках <> записываются параметры, которые применяются в функции (<int:category_id>)
]