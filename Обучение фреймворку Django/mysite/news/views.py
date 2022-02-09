from django.shortcuts import render
from django.http import HttpResponse
from news.models import News, Category

def index(request):
    news = News.objects.all()
    categories = Category.objects.all()
    return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей', 'categories': categories})

def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id) # Получаем только отфильтрованные новости, т.е. те, которые соответствуют выбранной категории
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'categories': categories, 'category': category})