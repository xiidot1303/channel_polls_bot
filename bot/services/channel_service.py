from app.services import *
from bot.models import Channel

def channels_all():
    query = Channel.objects.all()
    return query

def create_channel(title, id):
    channel_obj, created = Channel.objects.get_or_create(channel_id = id)
    channel_obj.title = title
    channel_obj.save()
    return channel_obj

def get_channel_by_title(title):
    channels = Channel.objects.filter(title=title)
    if channels:
        return channels[0]
    else:
        return None

def delete_channel(id):
    channel = Channel.objects.get(id=id)
    channel.polls.delete()
    channel.delete()
