from bot.bot import *


def _to_the_select_lang(update):
    update_message_reply_text(
        update,
        "Bot tilini tanlang\n\nВыберите язык бота",
        reply_markup=reply_keyboard_markup([lang_dict['uz_ru']]),
        
    )   
    return SELECT_LANG

def _to_the_get_name(update):
    update_message_reply_text(
        update=update,
        text=get_word("type name", update),
        reply_markup=reply_keyboard_markup([[get_word("back", update)]]),
    )
    return GET_NAME

def _to_the_get_contact(update):
    i_contact = KeyboardButton(
        text=get_word("leave number", update), request_contact=True
    )
    update_message_reply_text(
        update,
        get_word("send number", update),
        reply_markup=reply_keyboard_markup(
            [[i_contact], [get_word("back", update)]]
        ),
    )
    return GET_CONTACT


@is_start_registr
def select_lang(update, context):
    text = update.message.text
    if "UZ" in text:
        lang = "uz"
    elif "RU" in text:
        lang = "ru"
    else:
        return _to_the_select_lang(update)

    get_or_create(user_id=update.message.chat.id)
    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.lang = lang
    obj.save()

    return _to_the_get_name(update)


@is_start_registr
def get_name(update, context):
    if update.message.text == get_word("back", update):
        return _to_the_select_lang(update)

    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.name = update.message.text
    obj.username = update.message.chat.username
    obj.firstname = update.message.chat.first_name
    obj.save()

    return _to_the_get_contact(update)


@is_start_registr
def get_contact(update, context):
    if update.message.text == get_word("back", update):
        return _to_the_get_name(update)

    if update.message.contact == None or not update.message.contact:
        phone_number = update.message.text
    else:
        phone_number = update.message.contact.phone_number
    # check that phone is available or no
    is_available = Bot_user.objects.filter(phone=phone_number)
    if is_available:
        update.message.reply_text(get_word("number is logged", update))
        return GET_CONTACT
    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    main_menu(update, context)
    return ConversationHandler.END
