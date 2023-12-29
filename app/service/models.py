from django.core.validators import MinLengthValidator
from django.db import models


# Модель запроса к сервису
class Query(models.Model):
    created = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    kadastr_number = models.CharField(
        verbose_name='Кадастровый номер',
        max_length=254,
        unique=True,
        validators=[MinLengthValidator(3)]
    )
    latitude = models.FloatField(verbose_name='Широта', max_length=32)
    longitude = models.FloatField(verbose_name='Долгота', max_length=32)

    def __str__(self):
        return f'кадастровый номер: {self.kadastr_number}, широта: {self.latitude}, долгота: {self.longitude}'


# Модель ответа сервиса
class Result(models.Model):
    created = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    message = models.CharField(max_length=254)
    kadastr_number = models.CharField(max_length=254, blank=True, null=True)
    latitude = models.FloatField(max_length=32, blank=True, null=True)
    longitude = models.FloatField(max_length=32, blank=True, null=True)
    query = models.OneToOneField(Query, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'ответ: {self.message}'
