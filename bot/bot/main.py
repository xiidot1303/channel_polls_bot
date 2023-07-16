from bot.bot import *
from bot.bot.channels import to_the_channels_list

@check_user_access
def start(update, context):
    main_menu(update, context)

@check_user_access
def channels(update, context):
    return to_the_channels_list(update, context)