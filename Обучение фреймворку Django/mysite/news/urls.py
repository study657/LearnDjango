from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'), # Маршрут если используем класс
    # path('test/', test),
    # path('category/<int:category_id>/', get_category, name='category'), # В таких скобочках <> записываются параметры, которые применяются в функции (<int:category_id>)
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title': 'Какой-то title'}), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add_news/', add_news, name='add_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    path('test/', test, name='test'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]