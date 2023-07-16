from app.services import *
from bot.models import Poll, Option

def check_poll_title(channel, title):
    return Poll.objects.filter(title=title, channel__id=channel.id)

def create_poll(channel, title, photo, text, options):
    poll_obj = Poll.objects.create(
        channel = channel,
        title = title,
        photo = photo,
        text = text
    )
    for option in options:
        poll_obj.options.create(title=option)
    poll_obj.save()
    return poll_obj

def get_option_by_id(id) -> Option:
    obj = Option.objects.get(pk=id)
    return obj

def is_user_voted_to_poll(user_id, poll: Poll):
    return poll.voters.filter(user_id=user_id)

def vote_user(user_id, option: Option, poll: Poll):
    poll.voters.create(user_id=user_id, option=option)
    return