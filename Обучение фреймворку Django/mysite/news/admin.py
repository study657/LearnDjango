from django.contrib import admin
from .models import News, Category

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_field = ('title', 'content')
    list_editable = ('is_published',) # Указывается какое поле мы ходтим редактировать из админки
    list_filter = ('is_published', 'category') # Задается возможность фильтрации в админке по данным ячейкам

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_field = ('title',)

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)