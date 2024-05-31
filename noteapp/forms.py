from django import forms
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

from .models import *


class CleanFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs)


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class NoteForm(forms.ModelForm):
    content = forms.FileField(required=False)

    class Meta:
        model = Note
        fields = ['title', 'description', 'icon', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Мои проекты...'}),
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 70}),
            'icon': CleanFileInput(),
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].label = '*Название'
        self.fields['description'].label = 'Описание'
        self.fields['content'].label = 'Импорт содержимого'
        self.fields['icon'].label = 'Аватар'
        self.fields['category'].label = '*Категория'
        self.fields['category'].empty_label = None
        self.fields['category'].queryset = Category.objects.filter(author=self.author)

    def clean_content(self):
        content_file = self.cleaned_data.get('content')
        if content_file:
            filename = content_file.name.lower()
            if not filename.endswith('.md'):
                raise ValidationError('Файл должен иметь расширение .md')
        return content_file


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Учеба...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['color'].label = 'Цвет'


class NoteEditForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 1, 'class': 'note-text', 'placeholder': 'Начните писать здесь...', 'tabindex': -1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].strip = False


class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class NoteInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'icon', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 70}),
            'icon': CleanFileInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'
        self.fields['description'].label = 'Описание'
        self.fields['icon'].label = 'Аватар'
        self.fields['category'].label = 'Категория'
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['category'].queryset = Category.objects.all()

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')

        allowed_extensions = ['.jpg', '.png', '.gif']
        if not icon.name.lower().endswith(tuple(allowed_extensions)):
            raise ValidationError("Пожалуйста, загрузите изображение в формате .jpg, .png или .gif")

        return icon


class CategoryInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['color'].label = 'Цвет'


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': CleanFileInput()
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        try:
            with Image.open(avatar) as img:
                width, height = img.size

                # Проверка на квадратность
                if width != height:
                    raise ValidationError("Изображение должно быть квадратным")

                # Проверка на расширение файла
                allowed_extensions = ['.jpg', '.png', '.gif']
                if not avatar.name.lower().endswith(tuple(allowed_extensions)):
                    raise ValidationError("Пожалуйста, загрузите изображение в формате .jpg, .png или .gif")

        except Exception as e:
            raise ValidationError(e)

        return avatar


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['code_font', 'code_font_size', 'text_font', 'text_font_size', 'code_theme']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code_font'].label = 'Шрифт кода'
        self.fields['code_font_size'].label = 'Размер шрифта кода'
        self.fields['text_font'].label = 'Шрифт текста'
        self.fields['text_font_size'].label = 'Размер шрифта текста'
        self.fields['code_theme'].label = 'Тема кода'
