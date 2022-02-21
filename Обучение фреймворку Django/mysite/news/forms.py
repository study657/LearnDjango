from dataclasses import fields
from tkinter import Widget
from unicodedata import category
from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__' # Для того, чтобы отобразить все ячейки с БД, но на практике его использовать не рекоммендуется
        fields = ['title', 'content', 'is_published', 'category'] # Лучше перечислять все ячейки, которые мы хотим видеть
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }