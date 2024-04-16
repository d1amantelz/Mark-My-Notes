from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True, )
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons/%Y/%m/%d/', default='default/default-note-icon.png')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title} | {self.category} | {self.time_create:%d-%m-%Y | %H:%M:%S}'

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'note_id': self.pk})


class Category(models.Model):
    COLOR_CHOICES = [
        ('', 'Выберите цвет'),
        ('#264653', 'Темно-синий'),
        ('#2A9D8F', 'Циановый'),
        ('#E9C46A', 'Жёлтый'),
        ('#E76F51', 'Красный'),
        ('#F4A261', 'Оранжевый'),
        ('#A260CA', 'Фиолетовый'),
    ]

    name = models.CharField(max_length=20)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(choices=COLOR_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('change_category_info', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='default/default-profile-avatar.jpg')
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
