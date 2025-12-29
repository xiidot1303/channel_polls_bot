from app.views import *

def captcha_view(request):
    return render(request, "captcha/captcha.html")