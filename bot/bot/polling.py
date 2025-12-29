from bot.bot import *
from config import WEBAPP_URL


def _to_the_captcha(update: Update, context):
    option_id = context.user_data.get('option_id')
    # get option obj by id
    option_obj = get_option_by_id(int(option_id))
    poll_obj = option_obj.poll
    text = f"Siz dan rostdan ham <b>{poll_obj.title}</b> so'rovnomasi bo'yicha <code>{option_obj.title}</code> ga ovoz bermoqchimisiz?"
    markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Ovoz berishni tasdiqlash",
                            web_app=WebAppInfo(url=f"{WEBAPP_URL}/captcha"))]
        ],
        resize_keyboard=True
    )

    update.effective_message.reply_html(
        text=text,
        reply_markup=markup
    )

##################################################################


def get_vote(update: Update, context: ContextTypes):
    user_id = update.effective_user.id
    option_id = context.user_data.get('option_id')
    # get option obj by id
    option_obj = get_option_by_id(int(option_id))
    poll_obj = option_obj.poll
    if is_user_voted_to_poll(user_id, poll_obj):
        bot_send_message(update, context, 'Siz allaqachon ovoz bergansiz.')
        return

    text = "😊 Assalom alaykum.\nSo'rovnoma botga xush kelibsiz!"
    sponsor_channels = sponsor_channels_all()
    if sponsor_channels:
        send_sponsored_channels_list(update, context)
    else:
        return _to_the_captcha(update, context)



def send_sponsored_channels_list(update: Update, context: ContextTypes):
    if update.callback_query:
        update.effective_message.delete()
    unsubscribed_channels = unsubscribed_channels_of_user(
        context, update.effective_user.id)
    channels_count = len(unsubscribed_channels)
    if channels_count > 0:
        text = f"❕ Iltimos, so'rovnomada ishtirok etishingiz uchun quyidagi {channels_count} ta kanlaga a'zo bo'ling"
        inline_buttons = [
            [InlineKeyboardButton(text=channel.title, url=channel.invite_link)]
            for channel in unsubscribed_channels
        ]
        inline_buttons.append(
            [InlineKeyboardButton(
                text="✅ Obuna bo'ldim", callback_data='subscribed')]
        )
        inline_markup = InlineKeyboardMarkup(inline_buttons)
        update.effective_message.reply_text(text, reply_markup=inline_markup)
    else:
        # go to captcha
        return _to_the_captcha(update, context)


def verified_captcha(update: Update, context):
    user_id = update.effective_user.id
    option_id = context.user_data.get('option_id')
    # get option obj by id
    option_obj = get_option_by_id(int(option_id))
    poll_obj = option_obj.poll
    # update option counts
    option_obj.count += 1
    option_obj.save()
    vote_user(user_id, option_obj, poll_obj)
    # update count in channel message
    i_buttons = [
        [InlineKeyboardButton(text=f"{option.count} {option.title}",
                              url=f"https://t.me/{context.bot.get_me().username}?start=vote_{option.id}")]
        for option in poll_obj.options.filter().order_by('-count')
    ]
    markup =  InlineKeyboardMarkup(i_buttons)
    channel = poll_obj.channel
    bot: Bot = context.bot
    bot.edit_message_reply_markup(chat_id=channel.channel_id, message_id=poll_obj.msg_id, reply_markup=markup)
    # send message to user
    update.effective_message.reply_text(
        "✅ Sizning ovozingiz muvaffaqiyatli qabul qilindi!",
        reply_markup=ReplyKeyboardRemove())
    return
