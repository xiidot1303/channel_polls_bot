from django.db import models
from django.core.validators import FileExtensionValidator

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='', verbose_name='Имя')
    username = models.CharField(null=True, blank=True, max_length=256, verbose_name='username')
    firstname = models.CharField(null=True, blank=True, max_length=256, verbose_name='Никнейм')
    phone = models.CharField(null=True, blank=True, max_length=16, default='', verbose_name='Телефон')
    lang = models.CharField(null=True, blank=True, max_length=4, verbose_name='', default='uz')
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата регистрации')

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"
    
class Message(models.Model):
    bot_users = models.ManyToManyField('bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False, max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','bmp','gif'])]
    )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
        )
    file = models.FileField(null=True, blank=True, upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

class Channel(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name='Название')
    channel_id = models.BigIntegerField(null=True, blank=False, verbose_name='ID')

    @property
    def polls(self):
        query = Poll.objects.filter(channel__id = self.id)
        return query

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

class Vote(models.Model):
    user_id = models.BigIntegerField(null=True)
    option = models.ForeignKey('bot.Option', null=True, blank=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"

class Option(models.Model):
    title = models.CharField(blank=False, max_length=255, verbose_name='Название')
    count = models.IntegerField(default=0, verbose_name='Количество')

    @property
    def poll(self):
        obj = Poll.objects.get(options__id=self.id)
        return obj

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

class Poll(models.Model):
    channel = models.ForeignKey('bot.Channel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Канал')
    title = models.CharField(blank=False, max_length=255, verbose_name='Название')
    photo = models.FileField(null=True, blank=True, upload_to="poll/photo/", verbose_name='Фото')
    text = models.TextField(null=True, blank=True, max_length=4096, verbose_name='Текст')
    options = models.ManyToManyField(Option, verbose_name='Варианты')
    voters = models.ManyToManyField(Vote, verbose_name='Избиратели')
    msg_id = models.CharField(null=True, blank=True, max_length=32)
    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class SponsorChannel(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name='Название')
    channel_id = models.BigIntegerField(null=True, blank=False, verbose_name='ID')
    invite_link = models.CharField(null=True, blank=True, max_length=255, verbose_name='Пригласительная ссылка')

    class Meta:
        verbose_name = "Спонсорский канал"
        verbose_name_plural = "Спонсорские каналы"

    