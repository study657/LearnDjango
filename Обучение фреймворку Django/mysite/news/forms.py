from django import forms
from .models import News
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Имя пользователя должно состоять максимум из 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }

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


    def clean_title(self): # Для валидации создается данный метод
        title = self.cleaned_data['title'] # Получаем наш title, который хотим валидировать
        if re.match(r'\d', title): # Делаем проверку регулярным выражением на то, есть ли цифра в начале
            raise ValidationError('Название не должно начинаться с цифры') # Если есть, то вызываем ошибку, если нет, то возвращаем наш title
        return title