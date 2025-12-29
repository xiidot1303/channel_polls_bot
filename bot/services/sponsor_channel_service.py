from app.services import *
from bot.models import SponsorChannel
from bot.utils.bot_functions import *

def sponsor_channels_all():
    query = SponsorChannel.objects.all()
    return query

def create_sponsor_channel(title, id, invite_link):
    channel_obj, created = SponsorChannel.objects.get_or_create(channel_id = id)
    channel_obj.title = title
    channel_obj.invite_link = invite_link
    channel_obj.save()
    return channel_obj

def get_sponsor_channel_by_title(title):
    channels = SponsorChannel.objects.filter(title=title)
    if channels:
        return channels[0]
    else:
        return None

def delete_sponsor_channel(id):
    channel = SponsorChannel.objects.get(id=id)
    channel.delete()


def unsubscribed_channels_of_user(context: ContextTypes, user_id):
    bot: Bot = context.bot
    sponsor_channels = sponsor_channels_all()
    result = []
    for channel in sponsor_channels:
        chat_member = bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
        if chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR, ChatMember.MEMBER]:
            continue
        else:
            result.append(channel)

    return result
