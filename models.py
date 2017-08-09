# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


#class UserProfile(models.Model):

    #user = models.OneToOneField(User)
    #is_admin = models.BooleanField()
    #is_provider = models.BooleanField()
    #is_manager = models.BooleanField()


class Market(models.Model):

    name = models.CharField(max_length=200,verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рынок'
        verbose_name_plural = 'Рынки'


class Product(models.Model):

    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Sort(models.Model):

    product = models.ForeignKey(Product)
    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сорт'
        verbose_name_plural = 'Сорта'


class ProductUnit(models.Model):

    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Provider(models.Model):

    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.CharField(max_length=350,
                                   verbose_name='Краткое описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Price(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь')
    provider = models.ForeignKey(Provider, verbose_name='Поставщик')
    market = models.ForeignKey(Market, verbose_name='Рынок')
    product = models.ForeignKey(Product, verbose_name='Продукт')
    sort = models.ForeignKey(Sort, verbose_name='Сорт')
    product_unit = models.ForeignKey(ProductUnit,
                                     verbose_name='Единица измерения')
    price = models.FloatField(verbose_name='Цена, руб.')
    waggon_sign = models.CharField(max_length=6,verbose_name='Гос. ' \
                                                            'номер фуры')
    pub_date = models.DateTimeField(verbose_name='Дата создания')
    is_actual = models.BooleanField(verbose_name='Актуальность')

    def __str__(self):
        return self.market.name + ' - ' + self.provider.name + ' - ' + \
               self.product.name + ' - ' + self.sort.name + ' - ' + \
               str(self.price)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
