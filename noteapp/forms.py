from django import forms
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from django.core.exceptions import ValidationError

from .models import *


class CleanFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs)


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'icon', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 70}),
            'icon': CleanFileInput()
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'
        self.fields['description'].label = 'Описание'
        self.fields['icon'].label = 'Аватар'
        self.fields['category'].label = 'Категория'
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['category'].queryset = Category.objects.filter(author=self.author)


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': forms.Select(choices=[('', 'Выберите цвет')] + list(Category.COLOR_CHOICES))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['color'].label = 'Цвет'


class EditNoteForm(forms.ModelForm):
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


class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangeNoteInfoForm(forms.ModelForm):
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


class ChangeCategoryInfoForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': forms.Select(choices=[('', 'Выберите цвет')] + list(Category.COLOR_CHOICES))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['color'].label = 'Цвет'


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ChangeAvatarForm(forms.ModelForm):
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
