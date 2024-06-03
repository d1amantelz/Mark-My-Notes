import pytz
from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def user_localtime(value, user):
    if user.is_authenticated and value:
        # Преобразуйте значение времени в UTC, если оно не в UTC
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = timezone.make_aware(value, timezone=pytz.UTC)

        user_timezone = pytz.timezone(user.profile.timezone)
        return value.astimezone(user_timezone)
    return value
