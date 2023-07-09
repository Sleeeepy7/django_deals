from django.db import models


class Deal(models.Model):
    customer = models.CharField('Логин покупателя', max_length=255)
    item = models.CharField('Наименование товара', max_length=255)
    total = models.IntegerField('Сумма сделки', default=0)
    quantity = models.IntegerField('Кол-во товаров', default=0)
    date = models.DateTimeField('Дата и время регистрации сделки')
