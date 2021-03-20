from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender', verbose_name='Отправитель')
    resipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resipient', verbose_name='Получатель')
    message = models.TextField('Сообщение', max_length=5000)
    read = models.BooleanField('Прочитано', default=False)
    time = models.DateTimeField('Время создания', default=timezone.now)

    def __str__(self):
        return f'Отправитель: {self.sender.first_name}; Получатель: {self.resipient.first_name}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('time',)