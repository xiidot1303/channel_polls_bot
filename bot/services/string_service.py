from bot.services.language_service import get_word

def channel_info_string(update, channel):
    text = 'ℹ️ <b>{}</b>\n\n<b>{}</b>: {}\n<b>{}</b>: {}\n\n{}'.format(
        get_word('channel info', update),
        get_word('id', update),
        channel.channel_id,
        get_word('title', update),
        channel.title,
        get_word('poll actions', update),
    )
    return text