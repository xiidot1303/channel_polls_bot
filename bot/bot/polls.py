from bot.bot import *
from bot.bot.channels import to_the_channel_info
from telegram import ChatMember

def _to_the_adding_poll(update, context):
    text = get_word('type poll title', update)
    makrup  = reply_keyboard_markup([[get_word('back', update)]])
    update_message_reply_text(update, text, makrup)
    return GET_POLL_TITLE

def _to_the_getting_poll_photo(update, context):
    text = get_word('send poll photo', update)
    markup = reply_keyboard_markup([[
        get_word('back', update),
        get_word('skip', update),
    ]])
    update_message_reply_text(update, text, markup)
    return GET_POLL_PHOTO

def _to_the_getting_poll_text(update, context):
    # set user data photo as null, if message text is skip
    if update.message.text == get_word('skip', update):
        context.user_data['poll']['photo'] = None
    text = get_word('type poll text', update)
    makrup  = reply_keyboard_markup([[get_word('back', update)]])
    update_message_reply_text(update, text, makrup)
    return GET_POLL_TEXT

def _to_the_getting_poll_options(update, context):
    if query := update.callback_query:
        query.delete_message()
        update = query
    text = get_word('type poll options', update)
    makrup  = reply_keyboard_markup([[get_word('back', update)]])
    update_message_reply_text(update, text, makrup)
    return GET_POLL_OPTIONS


def _to_the_selecting_poll_sponsor_channels(update, context):
    text = get_word('select sponsor channels', update)
    channels = list(sponsor_channels_all().values_list('id', 'title'))
    i_buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"select-sponsor-channel-{id}")]
        for id, title in channels
    ]
    i_buttons.append(
        [
            InlineKeyboardButton(text=get_word('back', update), callback_data='back'),
            InlineKeyboardButton(text=get_word('next', update), callback_data='next'),
        ]
    )
    context.user_data['poll']['sponsor_channels_ids'] = []
    markup = InlineKeyboardMarkup(i_buttons)
    update_message_reply_text(update, text, reply_markup=markup)
    return SELECT_POLL_SPONSOR_CHANNELS


def _to_the_confirming_poll(update, context):
    if query := update.callback_query:
        query.delete_message()
        update = query
    options = context.user_data['poll']['options']
    i_buttons = [
        [InlineKeyboardButton(text=option, callback_data=option)]
        for option in options
    ]
    markup =  InlineKeyboardMarkup(i_buttons)
    poll_data = context.user_data['poll']
    send_newsletter(
        context.bot,
        update.message.chat.id,
        poll_data['text'],
        open('files/'+poll_data['photo'], 'rb') if poll_data['photo'] else None,
        reply_markup=markup
    )
    sponsor_channels_ids = context.user_data['poll']['sponsor_channels_ids']
    if sponsor_channels_ids:
        sponsor_channels = SponsorChannel.objects.filter(id__in=sponsor_channels_ids)
        sponsor_channels_text = f'{get_word("sponsor channels", update)}:\n'
        sponsor_channels_text += '\n'.join([channel.title for channel in sponsor_channels])
        context.bot.send_message(chat_id=update.message.chat.id, text=sponsor_channels_text)
    text = get_word('is message correct', update)
    keyboards = [[get_word('yes', update), get_word('no', update)], [get_word('back', update)]]
    update_message_reply_text(update, text, reply_markup=reply_keyboard_markup(keyboards))
    return CONFIRM_POLL


@is_start
def add_poll(update, context):
    return _to_the_adding_poll(update, context)

@is_start
def get_poll_title(update, context):
    msg_text = update.message.text
    channel = context.user_data['channel']
    if check_poll_title(channel, msg_text):
        text = get_word('this poll title is taken', update)
        update_message_reply_text(update, text)
        return 
    context.user_data['poll'] = {}
    context.user_data['poll']['title'] = msg_text
    return _to_the_getting_poll_photo(update, context)

@is_start
def get_poll_photo(update, context):
    # save photo and get photo path
    photo = save_and_get_photo(update, context)
    # save photo to user data
    context.user_data['poll']['photo'] = photo
    return _to_the_getting_poll_text(update, context)

@is_start
def get_poll_text(update, context):
    # get text of message
    msg_text = update.message.text
    # check message size
    photo = context.user_data['poll']['photo']
    if (len(msg_text) > 1024 and photo) or (len(msg_text) > 4096 and not photo):
        # message is too long for photo caption
        text = get_word('message text is too long', update)
        update_message_reply_text(update, text)
        return
    # save poll text 
    context.user_data['poll']['text'] = msg_text
    return _to_the_getting_poll_options(update, context)

@is_start
def get_poll_options(update, context):
    # get text of message
    msg_text = update.message.text
    options = msg_text.split('\n')
    options = list(filter(lambda x: x != '', options))
    # set options to user data
    context.user_data['poll']['options'] = options
    return _to_the_selecting_poll_sponsor_channels(update, context)


@is_start
def select_poll_sponsor_channel(update, context):
    if update.callback_query:
        query = update.callback_query
        update = query
        channel_id = int(query.data.split('-')[-1])
        sponsor_channels_ids = context.user_data['poll']['sponsor_channels_ids']
        if channel_id in sponsor_channels_ids:
            sponsor_channels_ids.remove(channel_id)
        else:
            sponsor_channels_ids.append(channel_id)
        context.user_data['poll']['sponsor_channels_ids'] = sponsor_channels_ids
        
        channels = list(sponsor_channels_all().values_list('id', 'title'))
        i_buttons = [
            [InlineKeyboardButton(
                text=title if id not in sponsor_channels_ids else f"✅ {title}",
                callback_data=f"select-sponsor-channel-{id}"
            )]
            for id, title in channels
        ]
        i_buttons.append(
            [
                InlineKeyboardButton(text=get_word('back', update), callback_data='back'),
                InlineKeyboardButton(text=get_word('next', update), callback_data='next'),
            ]
        )
        markup = InlineKeyboardMarkup(i_buttons)
        query.edit_message_reply_markup(reply_markup=markup)


@is_start
def confirm_poll(update, context):
    msg_text = update.message.text
    if msg_text == get_word('no', update):
        return _to_the_adding_poll(update, context)
    elif msg_text == get_word('yes', update):
        poll_data = context.user_data['poll']
        channel = context.user_data['channel']
        poll_obj = create_poll(
            channel, poll_data['title'], poll_data['photo'], 
            poll_data['text'], poll_data['options'], poll_data['sponsor_channels_ids']
            )
        # send poll to channel
        i_buttons = [
            [InlineKeyboardButton(text=f"{option.count} {option.title}", 
                                  url=f"https://t.me/{context.bot.get_me().username}?start=vote_{option.id}")]
            for option in poll_obj.options.filter().order_by('pk')
        ]
        markup =  InlineKeyboardMarkup(i_buttons)
        newsletter = send_newsletter(
            context.bot,
            channel.channel_id,
            poll_obj.text,
            poll_obj.photo,
            reply_markup=markup
        )
        poll_obj.msg_id = newsletter.message_id
        poll_obj.save()
        if newsletter:
            text = get_word('poll uploaded successfully', update)
            bot_send_message(update, context, text)
            return to_the_channel_info(update, context)
        else:
            try:
                bot_user = bot.get_me()
                chat_member = bot.get_chat_member(chat_id=channel.id, user_id=bot_user.id)
                if chat_member.status in [ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
                    text = get_word('error in sending message to channel', update)
                    bot_send_message(update, context, text)
                    return 
                else:
                    text = get_word('bot is not admin of this channel', update)    
                    update_message_reply_text(update, text)
                    delete_channel(channel.id)
                    main_menu(update, context)
                    return ConversationHandler.END
            except:
                text = get_word('bot is not member of this channel', update)
                update_message_reply_text(update, text)
                delete_channel(channel.id)
                main_menu(update, context)
                return ConversationHandler.END
        return