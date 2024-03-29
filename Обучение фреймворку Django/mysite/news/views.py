from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from news.models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin # Добавляем этот класс для ограничения доступа к полю "добавить новость" на сайте
from django.core.paginator import Paginator
from django.contrib import messages # Информационный модуль, который при каких=то действиях будет нам показывать информацию
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def contact(request): # Функция, которая создает пагинацию на нашей странице (нумерацию)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'mail@mail.ru', ['адресат1@mail.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})



def send_mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'mail@mail.ru', ['адресат1@mail.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, '')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


def register(request):
    if request.method == 'POST': # Если у нас метод POST, тогда мы создаем форму и заполняем ее данными из поста
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # Делаем реализацию автоматической авторизации пользователя после регистрации
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else: # В противном случае это будет не связанная форма
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = News # Будут полученны все данные из модели News
    template_name = 'news/home_news_list.html' # Переобределение базового файла. По умолчанию django создает файл с названием приложения + _list.html, но мы хотим свое название. Теперь шаблон news_list.html не используется
    context_object_name = 'news' # Указываем название того объекта с которым мы хотим работать, вместо базового object_list. Это все уже в шаблоне, когда проходим циклом. {% for item in object_list %}, теперь соответственно {% for item in news %}
    # extra_context = {'title': 'Главная',} # Этот атрибут желательно использовать только для статичных данных и нужен он для того, чтобы в шаблонах отображались переменные, ибо сейчас вот эта переменная без этого атрибута не выведется: {{ title }} :: {{ block.super }}, а когда мы задали этот атрибут, то уже увидим эту переменную
    mixin_prop = 'hello world'
    paginate_by = 2 # Две записи на странице должно показываться

    def get_context_data(self, **kwargs): # Данная функция уже позволяет нам получать переменные, но уже и те которые являются динамическими, т.е. изменяемыми, в общем улучшенная версия атрибута extra_context
        context = super().get_context_data(**kwargs) # Теперь в переменной записано все то, что было до этого
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self): # Данные метод переопределеяется в том случае, если нам нужна фильтрация по определенным данным. Например мы не хотим, чтобы если галочка не стоит в is_published, тогда новость бы не показывалась и вот тогда мы переопределяем этот метод
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False # Не разрешаем показ пустых списков. Нужно для того, чтобы если пользователь перейдет на id не существующей категории, чтобы не было ошибки 500, а была 404 ошибка
    paginate_by = 2 # Две записи на странице должно показываться

    def get_context_data(self, **kwargs): # Данная функция уже позволяет нам получать переменные, но уже и те которые являются динамическими, т.е. изменяемыми, в общем улучшенная версия атрибута extra_context
        context = super().get_context_data(**kwargs) # Теперь в переменной записано все то, что было до этого
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self): # Данные метод переопределеяется в том случае, если нам нужна фильтрация по определенным данным. Например мы не хотим, чтобы если галочка не стоит в is_published, тогда новость бы не показывалась и вот тогда мы переопределяем этот метод
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    pk_url_kwarg = 'news_id' # Наш pk или наш id он приходит в urls.py в виде параметра news_id
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm # Связывание нашей формы с классом, т.е. мы должны связаться с формой
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home') # Указание данного атрибута нужно для того, что если в модели мы не используем метод get_absolute_url, тогда после создания новости идет редирект на этот адрес
    login_url = '/admin/' # С помощью класса LoginRequiredMixin задали атрибут, который в случае попадания пользователя по ссылке, которая запрещена он будет перенаправлен на данный адрес




def test(request): # Функция, которая создает пагинацию на нашей странице (нумерацию)
    objects = ['John1', 'Paul2', 'George3', 'Ringo4', 'John5', 'Paul6', 'George7']
    paginator = Paginator(objects, 2) # Создали объект, с данными из objects и разбили их на 2 записи на каждой странице
    page_num = request.GET.get('page', 1) # Получили нашу текущую страницу, на которой находится пользователь. Если такая не найдена, то базово будет присвоена единичка (1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


# def index(request):
#     news = News.objects.all()
#     return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей',})

# def test(request):
#     return HttpResponse('<h1>Тестовая страница</h1>')

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id) # Получаем только отфильтрованные новости, т.е. те, которые соответствуют выбранной категории
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

# def add_news(request):
#     if request.method == 'POST': # При отправке данных из формы, т.е. когда идет метод POST - отправка данных
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data) # Сохранение данных в БД. ** - это распаковка словаря
#             news = form.save()
#             return redirect(news) # После успешной отправки формы делаем редирект на страничку home или же на созданный объект, в данном случае на созданную новость
#     else: # При рендеринге (показ формы при заходе на страницу, т.е. когда идет метод GET)
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})