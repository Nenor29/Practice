from django import forms
from .models import Article, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.widgets import CKEditorWidget  

class ArticleForm(forms.ModelForm):
    

    class Meta:
        model = Article
        
        fields = ['title', 'content', 'category', 'snippet']
        labels = {
            'title': "Название",
            'content': "Содержание",
            'category': "Категория",
            'snippet': "Описание",
        }
    def __init__(self, *args, **kwargs):
        parent_category = kwargs.pop('parent_category', None)
        super().__init__(*args, **kwargs)
        if parent_category:
          
            subcategories = Category.objects.filter(parent=parent_category)
            self.fields['category'].queryset = (
                Category.objects.filter(id=parent_category.id) |
                Category.objects.filter(parent=parent_category)
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': "Название",
            'description': "Описание"
        }
        
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    
    class Meta:
        model = User 
        fields = ("username", "password1", "password2")
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ("username", "password")
