from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from .forms import *
from .models import *


# ------- NOTE VIEWS -------

class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        user = self.request.user.profile
        return Note.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.profile
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'create_note.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user.profile})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('note_edit_mode', kwargs={'note_id': self.object.pk})


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteEditForm
    template_name = 'note.html'
    pk_url_kwarg = 'note_id'

    def get_success_url(self):
        return reverse_lazy('note_view_mode', kwargs={'note_id': self.object.pk})


class NoteViewMode(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'view_mode_note.html'
    pk_url_kwarg = 'note_id'


class NoteInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'update_note.html'
    pk_url_kwarg = 'note_id'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user.profile})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('note_edit_mode', kwargs={'note_id': self.object.pk})


class NotesByCategoryView(LoginRequiredMixin, ListView):
    template_name = 'notes_by_category.html'
    context_object_name = 'notes'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Note.objects.filter(category__pk=category_id, author=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


def delete_note(request, note_id):
    get_object_or_404(Note, pk=note_id).delete()
    return redirect('notes')


def export_note(request, note_id):
    note = Note.objects.get(id=note_id)
    response = HttpResponse(note.content, content_type='text/markdown')
    response['Content-Disposition'] = 'attachment; filename=note.md'
    return response


# ------- CATEGORY VIEWS -------

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        user = self.request.user.profile
        return Category.objects.filter(author=user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'create_category.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        if form.cleaned_data['color'] is None:
            form.instance.color = Category.COLOR_CHOICES[1][0]
        else:
            form.instance.color = form.cleaned_data['color']

        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'update_category.html'
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        if form.cleaned_data['color'] is None:
            form.instance.color = Category.COLOR_CHOICES[1][0]
        else:
            form.instance.color = form.cleaned_data['color']
        return super().form_valid(form)


def delete_category(request, category_id):
    get_object_or_404(Category, pk=category_id).delete()
    return redirect('/categories/')


# ------- PROFILE VIEWS -------

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserInfoUpdateForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

    def get_object(self, *args, **kwargs):
        return self.request.user


class UsernameUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsernameUpdateForm
    template_name = 'update_username.html'
    success_url = reverse_lazy('profile')

    def get_object(self, **kwargs):
        return self.request.user


class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = AvatarUpdateForm
    template_name = 'update_avatar.html'
    success_url = reverse_lazy('profile')

    def get_object(self, **kwargs):
        return self.request.user.profile


# ------- AUTH VIEWS -------

class SignUpPageView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('login')


class LoginPageView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('notes')


def logout_view(request):
    logout(request)
    return redirect('/login/')


# ------- OTHER VIEWS -------

def create_screen(request):
    return render(request, 'create_screen.html')


def note_search(request):
    search_query = request.POST.get('search')
    if search_query:
        notes = Note.objects.filter(Q(content__icontains=search_query) | Q(title__icontains=search_query))
        return render(request, 'note_search.html', {'notes': notes, 'search_query': search_query})
    else:
        return redirect(request.META.get('HTTP_REFERER', 'notes/'))
