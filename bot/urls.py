from django.urls import path

from bot.views import (
    botwebhook

)

from bot.views.captcha import captcha_view

from config import BOT_API_TOKEN

urlpatterns = [
    # bot
    path(BOT_API_TOKEN, botwebhook.bot_webhook),
    path("captcha", captcha_view),
]