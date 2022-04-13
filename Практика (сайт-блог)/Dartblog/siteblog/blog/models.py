from django.db import models
from django.urls import reverse

"""
Category
============
title - название категории
slug - url категории, т.е. если у нас категория назвается Жизнь, то будет адрсе домен/category/life

Tag
============
title - название тега
slug

Post
============
title
slug
author - автор поста
content
created_at - создание поста
photo
views - кол-во просмотров
category
tags
"""

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, verbose_name='Url Категории', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})
    

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=50, verbose_name='Url Тега', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название поста')
    slug = models.SlugField(max_length=255, verbose_name='Url Поста', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор поста')
    content = models.TextField(verbose_name='Контент', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликована')
    photo = models.ImageField(upload_to=f'photos/%Y/%m/%d/', blank=True, verbose_name='Пусть к фото')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']