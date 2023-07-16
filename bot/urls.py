from django.urls import path

from bot.views import (
    botwebhook

)

from config import BOT_API_TOKEN

urlpatterns = [
    # bot
    path(BOT_API_TOKEN, botwebhook.bot_webhook),
]