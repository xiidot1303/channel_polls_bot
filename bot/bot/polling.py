from bot.bot import *

def get_vote(update, context):
    update = update.callback_query
    if update.message.chat.type != 'channel':
        return
    user_id = update.from_user.id
    # check user is subscriber to bot or not
    chat_member = bot.get_chat_member(chat_id=update.message.chat.id, user_id=user_id)
    if chat_member.status == 'left':
        bot_answer_callback_query(update, context, "Ovoz berish uchun kanalga a'zo bo'ling")
        return
    option_id = update.data
    # get option obj by id
    option_obj = get_option_by_id(int(option_id))
    poll_obj = option_obj.poll
    if is_user_voted_to_poll(user_id, poll_obj):
        bot_answer_callback_query(update, context, 'Siz allaqachon ovoz bergansiz.')
        return
    # update option counts
    option_obj.count += 1
    option_obj.save()
    vote_user(user_id, option_obj, poll_obj)
    # update inline buttons
    i_buttons = [
        [InlineKeyboardButton(text='{} ➖ {}'.format(option.title, option.count), callback_data=str(option.id))]
        for option in poll_obj.options.filter().order_by('pk')
    ]
    markup =  InlineKeyboardMarkup(i_buttons)
    bot_edit_message_reply_markup(update, context, reply_markup=markup)
    return