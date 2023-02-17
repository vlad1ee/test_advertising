from django.db import models

from utils.models import AbstractModel

from .constants import ADVERTISING_STATUS_CHOICES


class Category(AbstractModel):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.slug


class Advertising(AbstractModel):
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=1,
                              choices=ADVERTISING_STATUS_CHOICES, blank=True)
    author = models.ForeignKey(to='user.User', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Рекламное объявление'
        verbose_name_plural = 'Рекламные объявления'
