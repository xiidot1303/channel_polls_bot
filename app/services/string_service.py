from app.services.language_service import get_string

def text_successfully_created(request):
    text = get_string('successfully created', request)  
    return text

def text_successfully_changed(request):
    text = get_string('successfully changed', request)  
    return text

def text_successfully_deleted(request):
    text = get_string('successfully deleted', request)
    return text