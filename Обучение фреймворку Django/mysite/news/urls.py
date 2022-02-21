from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'), # Маршрут если используем класс
    path('test/', test),
    path('category/<int:category_id>/', get_category, name='category'), # В таких скобочках <> записываются параметры, которые применяются в функции (<int:category_id>)
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/add_news/', add_news, name='add_news'),
]