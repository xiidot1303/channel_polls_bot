from django import template
from app.services import language_service
from app.utils import get_user_ip

register = template.Library()

@register.filter()
def string(request, text):
    text = text.lower()
    return language_service.get_string(text, request)

@register.filter()
def user_lang(request):
    ip = get_user_ip(request)
    return language_service.get_lang_by_ip(ip)