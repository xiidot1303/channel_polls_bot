from bot.bot import *
from telegram import ChatMember

def to_the_channels_list(update, context):
    channels = list(channels_all().values_list('title', flat=True))
    keyboards = [[get_word('main menu', update), get_word('add channel', update)]] + [[channel] for channel in channels]
    markup = reply_keyboard_markup(keyboards)
    update_message_reply_text(update, get_word('select channel', update), reply_markup=markup)
    return GET_CHANNEL_ACTION

def _to_the_adding_channel(update, context):
    text  = get_word('send channel id or username or forwarded message', update)
    markup = reply_keyboard_markup([[get_word('back', update)]])
    update_message_reply_text(update, text, reply_markup=markup)
    return GET_CHANNEL_ID

def to_the_channel_info(update, context):
    channel = context.user_data['channel']
    text = channel_info_string(update, channel)
    polls = list(channel.polls.values_list('title', flat=True))
    keyboards = [[get_word('back', update), get_word('add poll', update)]] + [polls]
    markup = reply_keyboard_markup(keyboards)
    update_message_reply_text(update, text, markup)
    return GET_POLL_ACTION_OR_DELETE_CHANNEL

@is_start
def select_channel(update, context):
    message_text = update.message.text
    channel = get_channel_by_title(message_text)
    if channel:
        # set channel to user data
        context.user_data['channel'] = channel
        return to_the_channel_info(update, context)
    else:
        text = get_word('select followed channels', update)
        update_message_reply_text(update, text)
        return
@is_start
def add_channel(update, context):
    return _to_the_adding_channel(update, context)

@is_start
def get_channel_id(update, context):
    # get bot object
    bot = context.bot
    # get channel if from text or get forwarded from chat  id if message is forwarded
    if update.message.forward_from_chat:
        channel_id = update.message.forward_from_chat.id
    elif update.message.text == get_word('back', update):
        return to_the_channels_list(update, context)
    else:
        channel_id = update.message.text

    # get bot object details
    bot_user = bot.get_me()
    try:
        chat = bot.get_chat(chat_id=channel_id)
        # check chat type, if chat type is not channel, then return function
        if chat.type != 'channel':
            text = get_word('send only channel id', update)
            update_message_reply_text(update, text)
            return
        # get status of bot in channel
        chat_member = bot.get_chat_member(chat_id=channel_id, user_id=bot_user.id)
        # check status
        if chat_member.status in [ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
            channel = chat
            # create channel obj
            create_channel(channel.title, channel.id)
            text = get_word('channel added successfully', update)
            update_message_reply_text(update, text)
        else:
            text = get_word('promote bot to admin', update)
            update_message_reply_text(update, text)
            return
    except:
        # chat is not found, return function
        text = get_word('channel is not found', update)
        update_message_reply_text(update, text)
        return

    return to_the_channels_list(update, context)