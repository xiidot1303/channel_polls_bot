from bot.bot import *
from bot.bot.channels import to_the_channels_list
from bot.bot.sponsor_channels import to_the_sponsor_channels_list
from bot.bot.polling import get_vote

@check_user_access
def start(update: Update, context):
    msg = update.effective_message.text
    if msg != '/start':
        start_msg = msg.split(' ')[1]
        *args, option_id = start_msg.split('_')
        context.user_data['option_id'] = option_id
        get_vote(update, context)
        return
    
    main_menu(update, context)

@check_user_access
def channels(update, context):
    return to_the_channels_list(update, context)

@check_user_access
def sponsor_channels(update, context):
    return to_the_sponsor_channels_list(update, context)