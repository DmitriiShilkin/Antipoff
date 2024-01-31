import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Query, Result
from .serializers import QuerySerializer, ResultSerializer


# Тест для проверки функционала нашего API
class QueryTest(APITestCase):
    # создаем данные, с которыми будем работать в последующих тестах
    def setUp(self):
        # два объекта запроса:
        # первый запрос
        self.query1 = Query.objects.create(
            kadastr_number='47:14:1203001:814',
            latitude=29.8621823,
            longitude=59.7295251
        )

        # второй запрос
        self.query2 = Query.objects.create(
            kadastr_number='6310138500:10:012:0045',
            latitude=49.98081,
            longitude=36.25272
        )

        # три объекта ответа:
        # первый ответ
        self.result1 = Result.objects.create(
            message='True',
            query=self.query1
        )

        # второй ответ
        self.result2 = Result.objects.create(
            message='False',
            query=self.query2
        )

        # третий ответ
        self.result3 = Result.objects.create(
            message='False',
            kadastr_number='77:06:0003009:1046'
        )

    # проверяем получение истории всех записей о запросах
    def test_history_list(self):
        response = self.client.get(reverse('history-list'))
        serializer_data = QuerySerializer(Query.objects.all(), many=True).data
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка количества созданных записей запросов
        self.assertEqual(len(response.data.get('results')), 2)
        # проверка соответствия запрошенных и полученных данных
        self.assertEqual(serializer_data, response.data.get('results'))

    # проверяем получение истории записи о втором запросе
    def test_history_detail(self):
        response = self.client.get(reverse('history-detail', kwargs={'pk': self.query2.id}))
        serializer_data = QuerySerializer(self.query2).data
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка соответствия запрошенных и полученных данных
        self.assertEqual(serializer_data, response.data)

    # проверяем отсутствие создания записи о запросе при незаполненных обязательных полях
    def test_null_create(self):
        data = {
            'kadastr_number': '',
            'latitude': None,
            'longitude': None,
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('query-list'), data=json_data, content_type='application/json')
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка количества созданных записей о запросах
        self.assertEqual(Query.objects.all().count(), 2)

    # проверяем отсутствие создания записи о запросе при повторной отправке уже существующего кадастрового номера
    def test_not_unique_create(self):
        data = {
            'kadastr_number': '47:14:1203001:814',
            'latitude': 31.5621823,
            'longitude': 49.8295251,
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('query-list'), data=json_data, content_type='application/json')
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка количества созданных записей о запросах
        self.assertEqual(Query.objects.all().count(), 2)

    # проверяем получение всех записей об ответах
    def test_result_list(self):
        response = self.client.get(reverse('result-list'))
        serializer_data = ResultSerializer(Result.objects.all(), many=True).data
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка количества созданных записей об ответах
        self.assertEqual(len(response.data.get('results')), 3)
        # проверка соответствия запрошенных и полученных данных
        self.assertEqual(serializer_data, response.data.get('results'))

    # проверяем получение записи о первом ответе
    def test_result_detail(self):
        response = self.client.get(reverse('result-detail', kwargs={'pk': self.result1.id}))
        serializer_data = ResultSerializer(self.result1).data
        # проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка соответствия запрошенных и полученных данных
        self.assertEqual(serializer_data, response.data)
