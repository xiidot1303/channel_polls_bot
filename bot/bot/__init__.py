from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.services.string_service import *
from bot.services.channel_service import *
from bot.services.sponsor_channel_service import *
from bot.services.poll_service import *
from bot.resources.conversationList import *

def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing

    bot = context.bot
    keyboard = [
        [get_word('channels', update)],
        [get_word('sponsor channels', update)],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    bot.send_message(
        update.message.chat.id,
        get_word("main menu", update),
        reply_markup=reply_markup,
    )
    check_username(update)

def make_button_settings(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing
    bot = context.bot

    bot.send_message(
        update.message.chat.id,
        get_word("settings desc", update),
        reply_markup=ReplyKeyboardMarkup(keyboard=settings_keyboard(update), resize_keyboard=True),
    )





# DECORATORS

def is_start_registr(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except:
            update = args[0].callback_query
            data = update.data
        id = update.message.chat.id
        if update.message.text == "/start":
            update.message.reply_text(
                lang_dict['hello'],
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True
                ),
            )
            return SELECT_LANG

        else:
            return func(*args, **kwargs)

    return func_arguments


def is_start(func):  # This deco break registration if user send /start.
    def func_arguments(*args, **kwargs):
        context = args[1]
        bot = context.bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except Exception:
            try:
                update = args[0].callback_query
                data = update.data
            except:
                return func(*args, **kwargs)
                
        id = update.message.chat.id
        if (
            update.message.text == "/start"
            or data == "main_menu"
            or update.message.text == get_word("main menu", update)
        ):
            if data == 'main_menu':
                bot_delete_message(update, context)
            # some func
            remove_inline_keyboards_from_last_msg(update, context)
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)

    return func_arguments

def ignore_start(func):
    def func_arguments(*args, **kwargs):
        context = args[1]
        bot = context.bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except Exception:
            try:
                update = args[0].callback_query
                data = update.data
            except:
                return func(*args, **kwargs)
                
        id = update.message.chat.id
        if (
            update.message.text == "/start"
            or update.message.text == get_word("main menu", update)
        ):
            # some func
            remove_inline_keyboards_from_last_msg(update, context)
            message, markup = get_last_msg_and_markup(context)
            if message.photo:
                    bot.send_photo(
                        update.message.chat.id,
                        message.photo[0]['file_id'],
                        caption=message.caption,
                        reply_markup=markup,     
                    )
            else:
                update_message_reply_text(update, message.text, reply_markup=markup)
            return
        elif data == "main_menu":
            bot_delete_message(update, context)
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)

    return func_arguments

def check_user_access(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        update: Update = args[0]
        
        id = update.effective_user.id
        message_text = update.effective_message.text
        if is_user_allowed(id) or message_text != '/start':
            return func(*args, **kwargs)
        else:
            update_message_reply_text(update, 'Sorry, you do not have permission to use the bot')
            return ConversationHandler.END
    return func_arguments