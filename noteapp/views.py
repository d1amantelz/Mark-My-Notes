from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *


def notes(request):
    user = Profile.objects.get(user=request.user)
    context = {'notes': Note.objects.filter(author=user),
               'user': user}
    return render(request, 'notes.html', context=context)


def create_note(request):
    if request.method == 'POST':
        form = CreateNoteForm(request.POST, request.FILES, author=request.user.profile)

        if form.is_valid():
            print(form.cleaned_data)
            note = Note.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                author=Profile.objects.get(user=request.user),
                icon=form.cleaned_data['icon'],
                category=form.cleaned_data['category'])
            note.save()
            return redirect(f'/note_detail/{note.pk}')
    else:
        form = CreateNoteForm(author=request.user.profile)

    return render(request, 'create_note.html', context={'form': form})


def note_detail(request, note_id):
    note = Note.objects.get(pk=note_id)

    if request.method == 'POST':
        form = EditNoteForm(request.POST)

        if form.is_valid():
            note.content = form.cleaned_data['content']
            note.save()
            return redirect(f'/note/{note.pk}/view_mode/')
    else:
        form = EditNoteForm(instance=note)

    return render(request, 'note.html', context={'note': note, 'form': form})


def note_view_mode(request, note_id):
    note = Note.objects.get(pk=note_id)
    return render(request, 'view_mode_note.html', context={'note': note})


def profile_view(request):
    profile = Profile.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = ChangeUserInfoForm(instance=request.user)

    return render(request, 'profile.html', {'profile': profile, 'form': form})


def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = ChangeUsernameForm(instance=request.user)

    return render(request, 'change_username.html', {'form': form})


def change_avatar(request):
    profile = Profile.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('/profile/')
    else:
        form = ChangeAvatarForm(instance=profile)

    return render(request, 'change_avatar.html', {'form': form})


def change_note_info(request, note_id):
    note = Note.objects.get(pk=note_id)

    if request.method == 'POST':
        form = ChangeNoteInfoForm(request.POST, request.FILES)
        if form.is_valid():

            print(form.cleaned_data)
            note.title = form.cleaned_data['title']
            note.description = form.cleaned_data['description']
            note.category = form.cleaned_data['category']

            if form.cleaned_data['icon'] != 'default/default-note-icon.png':
                note.icon = form.cleaned_data['icon']

            note.author = request.user.profile
            note.save()

            return redirect(f'/note_detail/{note.pk}')
    else:
        form = ChangeNoteInfoForm(instance=note)

    return render(request, 'change_note_info.html', {'form': form})


def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.delete()
    return redirect('/')


def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('/categories/')


def logout_view(request):
    logout(request)
    return redirect('login')


class SignUpPageView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('login')


class LoginPageView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('notes')


def categories(request):
    categories = Category.objects.filter(author=Profile.objects.get(user=request.user))
    return render(request, 'categories.html', context={'categories': categories})


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, 'category.html', context={'category': category})


def create_screen(request):
    return render(request, 'create_screen.html')


def create_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)

            category = Category.objects.create(
                name=form.cleaned_data['name'],
                author=Profile.objects.get(user=request.user))

            if form.cleaned_data['color'] is None:
                category.color = Category.COLOR_CHOICES[1][0]
            else:
                category.color = form.cleaned_data['color']

            category.save()
            return redirect('/categories')
    else:
        form = CreateCategoryForm()

    return render(request, 'create_category.html', context={'form': form})


def change_category_info(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        form = ChangeCategoryInfoForm(request.POST, request.FILES)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.color = form.cleaned_data['color']
            category.save()
            return redirect('/categories/')
    else:
        form = ChangeCategoryInfoForm(instance=category)

    return render(request, 'change_category_info.html', {'form': form})


def notes_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    notes_by_cat = Note.objects.filter(category__pk=category_id, author=request.user.profile)
    return render(request, 'notes_by_category.html', context={'notes': notes_by_cat, 'category': category})
