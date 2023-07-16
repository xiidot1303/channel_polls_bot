from telegram import Bot, InputTextMessageContent
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence, BasePersistence
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    BaseFilter
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *
from bot.bot import (
    main, login, settings, channels, polls, polling
)

start_handler = CommandHandler("start", main.start)

channels_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict['channels']), main.channels)],
    states={
        GET_CHANNEL_ACTION: [
            MessageHandler(Filters.text(lang_dict['add channel']), channels.add_channel),
            MessageHandler(Filters.text, channels.select_channel),
            ],
        GET_CHANNEL_ID: [
            MessageHandler(Filters.text, channels.get_channel_id),
            ],
        GET_POLL_ACTION_OR_DELETE_CHANNEL: [
            MessageHandler(Filters.text(lang_dict['add poll']), polls.add_poll),
            CommandHandler('start', polls.add_poll),
            MessageHandler(Filters.text(lang_dict['back']), channels.to_the_channels_list),

            ],
        GET_POLL_TITLE: [
            MessageHandler(Filters.text(lang_dict['back']), channels.to_the_channel_info),
            MessageHandler(Filters.text, polls.get_poll_title),

            ],
        GET_POLL_PHOTO: [
            MessageHandler(Filters.text(lang_dict['back']), polls._to_the_adding_poll),
            MessageHandler(Filters.text(lang_dict['skip']), polls._to_the_getting_poll_text),
            MessageHandler(Filters.photo, polls.get_poll_photo),
            CommandHandler('start', polls.get_poll_photo),
        ],
        GET_POLL_TEXT: [
            MessageHandler(Filters.text(lang_dict['back']), polls._to_the_getting_poll_photo),
            MessageHandler(Filters.text, polls.get_poll_text),
        ],
        GET_POLL_OPTIONS: [
            MessageHandler(Filters.text(lang_dict['back']), polls._to_the_getting_poll_text),
            MessageHandler(Filters.text, polls.get_poll_options),
        ],
        CONFIRM_POLL: [
            MessageHandler(Filters.text(lang_dict['back']), polls._to_the_getting_poll_options),
            MessageHandler(Filters.text, polls.confirm_poll),
        ]
    },
    fallbacks=[],
    name='channels',
    persistent=True
)

polling_handler = CallbackQueryHandler(polling.get_vote)

handlers = [
    polling_handler,
    start_handler,
    channels_handler,
]