from django import template
from news.models import Category
from django.db.models import Count, F

register = template.Library()

@register.simple_tag(name='get_list_categiries') # Декоратор. Нужен для возможности отмены поведения функции
def get_categiries(): # Создание простого тега simple tag, который просто может выводить данные
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html') # Тег и параметром передается где он создан
def show_categories(arg1='Hello', arg2='world'): # Создание уже сложного тега, который может и выводить данные и рендерить их, т.е. отображать
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0) # С помощью метода annotate выводим только те категории, в которых есть записи (новости)
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}