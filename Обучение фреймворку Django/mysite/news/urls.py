from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', index, name='home'),
    path('', cache_page(60)(HomeNews.as_view()), name='home'), # Маршрут если используем класс
    # path('test/', test),
    # path('category/<int:category_id>/', get_category, name='category'), # В таких скобочках <> записываются параметры, которые применяются в функции (<int:category_id>)
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title': 'Какой-то title'}), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add_news/', add_news, name='add_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    path('test/', send_mail, name='test'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'), # Выход пользователя
    path('contact/', contact, name='contact'),
]