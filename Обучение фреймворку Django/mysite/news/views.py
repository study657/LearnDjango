from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from news.models import News, Category
from .forms import NewsForm

def index(request):
    news = News.objects.all()
    return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей',})

def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id) # Получаем только отфильтрованные новости, т.е. те, которые соответствуют выбранной категории
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    if request.method == 'POST': # При отправке данных из формы
        pass
    else: # При рендеринге (показ формы при заходе на страницу)
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})