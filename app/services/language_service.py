from app.services import *
from app.models import Language
from app.resources.strings import lang_dict

def get_string(text, request):
    ip = get_user_ip(request)
    lang = get_lang_by_ip(ip)
    if text in lang_dict:
        string = lang_dict[text][lang]
    else:
        string = text
    return string

def get_language_by_ip(ip):
    return Language.objects.get(user_ip=ip)

def get_lang_by_ip(ip):
    lang_tuple = Language.objects.get_or_create(user_ip=ip)
    lang_obj = lang_tuple[0]
    if lang_tuple[1]:
        lang_obj.lang = 1
        lang_obj.save()
    return lang_obj.lang

def update_lang_by_ip(ip, lang: int):
    lang_obj = get_language_by_ip(ip)
    lang_obj.lang = lang
    lang_obj.save()
    return lang_obj