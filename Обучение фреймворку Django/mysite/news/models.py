from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата правки')
    photo = models.ImageField(upload_to=f'photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликованно')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория') # Связывание этой области с таблицей категорий. Параметр null нужен потому, что мы уже ранее создали таблицу и без этого параметра ее просто нельзя будет поменять, т.к. данных то там нет, а мы добавляем новое поле

    def my_func(self):
        return 'Hello from model'

    def get_absolute_url(self): # Благодаря этому методу, если мы работаем с классами в views.py то происходит при добавлении чего-то в БД редирект на эту самую новость, которую мы добавили
        return reverse("view_news", kwargs={"news_id": self.pk})

    def __str__(self): # Функция, которая показывает строковое представление объектов
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']



class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.pk})
    

    def __str__(self): # Функция, которая показывает строковое представление объектов
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']