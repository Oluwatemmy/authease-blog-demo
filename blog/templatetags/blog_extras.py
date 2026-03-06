from django import template

register = template.Library()


@register.filter
def reading_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


@register.filter
def avatar_url(user):
    if user.profile_picture:
        return user.profile_picture.url
    return f"https://api.dicebear.com/9.x/initials/svg?seed={user.first_name}+{user.last_name}&radius=50&backgroundColor=0d6efd"


@register.filter
def initials(user):
    first = user.first_name[0].upper() if user.first_name else ''
    last = user.last_name[0].upper() if user.last_name else ''
    return f"{first}{last}"
