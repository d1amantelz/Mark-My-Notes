from collections import defaultdict
from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
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
        pinned_notes = Note.objects.filter(author=user, is_deleted=False, is_pinned=True).order_by('-time_update')
        other_notes = Note.objects.filter(author=user, is_deleted=False, is_pinned=False).order_by('-time_update')
        all_notes = list(pinned_notes) + list(other_notes)
        return all_notes


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
        content_file = self.request.FILES.get('content')
        if content_file:
            form.instance.content = content_file.read().decode('utf-8')
        Activity.objects.create(user=self.request.user.profile, action='create_note')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('note_edit_mode', kwargs={'note_id': self.object.pk})


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteEditForm
    template_name = 'note.html'
    pk_url_kwarg = 'note_id'

    def get_success_url(self):
        Activity.objects.create(user=self.request.user.profile, action='edit_note')
        return reverse_lazy('note_view_mode', kwargs={'note_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = Setting.objects.get(user=self.request.user.profile)
        context['settings'] = settings
        context['url'] = self.request.build_absolute_uri(
            reverse('note_view_mode',
                    kwargs={'note_id': self.object.pk}))
        context['text'] = 'Посмотри мою заметку!'
        context['note_id'] = self.object.pk
        return context


class NoteViewMode(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'view_mode_note.html'
    pk_url_kwarg = 'note_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = Setting.objects.filter(user=self.request.user.profile).first()
        if settings:
            context['settings'] = settings
        return context


class NoteInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteInfoUpdateForm
    template_name = 'update_note.html'
    pk_url_kwarg = 'note_id'

    def get_success_url(self):
        return reverse_lazy('note_edit_mode', kwargs={'note_id': self.object.pk})


class NotesByCategoryView(LoginRequiredMixin, ListView):
    template_name = 'notes_by_category.html'
    context_object_name = 'notes'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Note.objects.filter(category__pk=category_id, author=self.request.user.profile, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


def delete_note(request, note_id):
    get_object_or_404(Note, pk=note_id).delete()
    Activity.objects.create(user=request.user.profile, action='delete_note')
    return redirect('notes')


def export_note(request, note_id):
    note = Note.objects.get(id=note_id)
    response = HttpResponse(note.content, content_type='text/markdown')
    response['Content-Disposition'] = 'attachment; filename=note.md'
    return response


# TODO: refactor this function to a class view
def note_search(request):
    search_query = request.POST.get('search')
    if search_query:
        notes = Note.objects.filter(
            Q(content__icontains=search_query) | Q(title__icontains=search_query),
            author=request.user.profile,
            is_deleted=False)
        settings = Setting.objects.get(user=request.user.profile)
        return render(request, 'note_search.html',
                      {'notes': notes,
                       'search_query': search_query,
                       'settings': settings})
    else:
        return redirect(request.META.get('HTTP_REFERER', 'notes/'))


class TrashListView(LoginRequiredMixin, ListView):
    template_name = 'trash_notes.html'
    context_object_name = 'trash_notes'

    def get_queryset(self):
        user = self.request.user.profile
        return Note.objects.filter(author=user, is_deleted=True)


def delete_permanently_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete_permanently()
    return redirect('trash')


def restore_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.restore()
    Activity.objects.create(user=request.user.profile, action='restore_note')
    return redirect('trash')


def duplicate_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    duplicated_note = Note.objects.create(
        title=note.title + ' (copy)',
        description=note.description,
        content=note.content,
        author=note.author,
        icon=note.icon,
        category=note.category)
    duplicated_note.save()

    return redirect('note_edit_mode', duplicated_note.pk)


def pin_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.pin()
    return redirect('note_edit_mode', note.pk)


def unpin_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.unpin()
    return redirect('note_edit_mode', note.pk)


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
        Activity.objects.create(user=self.request.user.profile, action='create_category')
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

        Activity.objects.create(user=self.request.user.profile, action='edit_category')
        return super().form_valid(form)


def delete_category(request, category_id):
    get_object_or_404(Category, pk=category_id).delete()
    Activity.objects.create(user=request.user.profile, action='delete_category')
    Activity.objects.create(user=request.user.profile, action='delete_note')
    return redirect('/categories/')


# ------- PROFILE VIEWS -------

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserInfoUpdateForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile

        # Получаем активности пользователя
        activities = Activity.objects.filter(user=profile)

        # Группируем активности по дате
        activities_by_date = defaultdict(list)
        for activity in activities:
            activities_by_date[activity.date].append(activity.action)

        # Получаем диапазон дат для отображения статистики
        today = timezone.now().date()
        start_date = today - timedelta(days=6)  # Неделя назад от сегодняшнего дня
        date_range = [start_date + timedelta(days=i) for i in range(7)]

        # Создаем словарь для отображения активности по датам
        activities_display = {date: (date in activities_by_date) for date in date_range}

        context['activities'] = activities_display
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


# ------- OTHER VIEWS -------

@login_required
def create_screen(request):
    return render(request, 'create_screen.html')


def help_view(request):
    return render(request, 'help.html')


@login_required
def feedback_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        if title and description:
            report = Report.objects.create(
                title=title,
                description=description,
                author=request.user.profile)

            for image in images:
                ReportImage.objects.create(report=report, image=image)

            return redirect('notes')

    return render(request, 'feedback.html')


class SettingsUpdateView(UpdateView):
    model = Setting
    form_class = SettingForm
    template_name = 'settings.html'
    success_url = reverse_lazy('notes')

    def get_object(self, **kwargs):
        return Setting.objects.get(user=self.request.user.profile)
