from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.utils import timezone


class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, default='')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons/%Y/%m/', blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    def pin(self):
        self.is_pinned = True
        self.save()

    def unpin(self):
        self.is_pinned = False
        self.save()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def delete_permanently(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.title} | {self.category} | {self.time_create:%d-%m-%Y | %H:%M:%S}'

    def get_absolute_url(self):
        return reverse('note_edit_mode', kwargs={'note_id': self.pk})


class Category(models.Model):
    COLOR_CHOICES = [
        ('#264653', 'Темно-синий'),
        ('#2A9D8F', 'Циановый'),
        ('#E9C46A', 'Жёлтый'),
        ('#E76F51', 'Красный'),
        ('#F4A261', 'Оранжевый'),
        ('#A260CA', 'Фиолетовый'),
    ]

    name = models.CharField(max_length=20)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    color = models.CharField(choices=COLOR_CHOICES, default='#264653')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('update_category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    settings = models.ForeignKey('Setting', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Setting(models.Model):
    FONT_CHOICES = [
        ('JetBrains Mono', 'JetBrains Mono'),
        ('Nunito', 'Nunito'),
        ('Fira Code', 'Fira Code'),
        ('Roboto Thin', 'Roboto Thin'),
        ('Source Code Pro', 'Source Code Pro'),
    ]

    FONT_SIZE_CHOICES = [
        (12, '12'),
        (14, '14'),
        (16, '16'),
        (18, '18'),
    ]

    CODE_THEME_CHOICES = [
        ('a11y-dark', 'a11y-dark'),
        ('atom-one-dark', 'atom-one-dark'),
        ('isbl-editor-dark', 'isbl-editor-dark'),
        ('agate', 'agate'),
    ]

    user = models.OneToOneField('Profile', on_delete=models.CASCADE, unique=True)
    code_font = models.CharField(max_length=20, choices=FONT_CHOICES, default='JetBrains Mono')
    code_font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    text_font = models.CharField(max_length=20, choices=FONT_CHOICES, default='JetBrains Mono')
    text_font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=16)
    code_theme = models.CharField(max_length=20, choices=CODE_THEME_CHOICES, default='a11y-dark')

    def __str__(self):
        return f"{self.user}'s settings"


class Activity(models.Model):
    ACTION_CHOICES = [
        ('create_note', 'Создание заметки'),
        ('edit_note', 'Редактирование заметки'),
        ('delete_note', 'Удаление заметки'),
        ('restore_note', 'Восстановление заметки'),
        ('create_category', 'Создание категории'),
        ('edit_category', 'Редактирование категории'),
        ('delete_category', 'Удаление категории'),
    ]

    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user.username} - {self.action} - {self.date}"


class Report(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ReportImage(models.Model):
    report = models.ForeignKey('Report', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reports/%Y/%m/')

    def __str__(self):
        return f"Image for {self.report.title}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        settings = Setting.objects.create(user=profile)
        profile.settings = settings
        profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user_settings(sender, instance, **kwargs):
    if instance.settings:
        instance.settings.delete()
