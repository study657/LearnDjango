from django.contrib import admin
from .models import News, Category
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget()) # Для этого поля идет переопределение и добавление собственно нашего визуального редактора в админке

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm # Подключаем данный класс к нашей форме админки
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_field = ('title', 'content')
    list_editable = ('is_published',) # Указывается какое поле мы ходтим редактировать из админки
    list_filter = ('is_published', 'category') # Задается возможность фильтрации в админке по данным ячейкам
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'created_at', 'updated_at') # Указываются те поля, которые должны быть отображены внутри нашей новости при ее редактировании в админке
    readonly_fields = ('get_photo', 'created_at', 'updated_at') # Данные поля мы помечаем, что они могут быть только для чтения и что их менять нельзя. Потому что эти поля создаются в момент создания и менять их категорически запрещено, да и вообще мы не хотим этого
    save_on_top = True # Сделать так, чтобы панелька для сохраниния записи после редактирования была не только внизу, но и наверху

    def get_photo(self, obj): # Создаем метод, который будет в нашей админке создавать тег img с фотографией в ней
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'Фото не установлено'

    get_photo.short_description = 'Миниатюра фото' # Позволяет заменить нам название самой ячейки за место названия get_photo

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_field = ('title',)

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями' # Изменить(переопределить) title (название) страницы
admin.site.site_header = 'Управление новостями' # Изменить(переопределить) заголовок на самой странице