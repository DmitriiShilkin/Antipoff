import sys
import time
import requests
import random

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Query, Result
from .serializers import QuerySerializer, ResultSerializer


# Представление для эмулятора внешнего сервера
class ExternalServerEmulatorView(APIView):

    def post(self, request):
        serializer_context = {
            'request': request
        }
        serializer = QuerySerializer(data=request.data, context=serializer_context)

        # эмуляция обработки запроса внешним сервером
        time.sleep(60)
        result = random.choice([True, False])

        if serializer.is_valid():
            serializer.save()
            Result.objects.create(
                message=result,
                query=Query.objects.get(id=serializer.data.get('id'))
            )

            return Response(
                {
                    'result': result,
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            Result.objects.create(
                message=serializer.errors,
                kadastr_number=serializer.data.get('kadastr_number'),
                latitude=serializer.data.get('latitude'),
                longitude=serializer.data.get('longitude')
            )
            return Response(
                {
                    'result': result,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            Result.objects.create(
                message='Internal Server Error',
                kadastr_number=serializer.data.get('kadastr_number'),
                latitude=serializer.data.get('latitude'),
                longitude=serializer.data.get('longitude')
            )
            return Response(
                {
                    'result': result,
                }
            )


# Представление для обработки запросов пользователя
class QueryViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = QuerySerializer

    def create(self, request, *args, **kwargs):

        # Здесь эмулируется отправка запроса на внешний сервер
        response = requests.post(
            url='http://localhost:8000' + reverse_lazy('emulate-external-server'),
            data={
                'kadastr_number': request.data.get('kadastr_number'),
                'latitude': request.data.get('latitude'),
                'longitude': request.data.get('longitude')
            }
        )
        # Здесь эмулируется получение ответа от внешнего сервера
        result = response.json().get('result')
        return Response(
            {
                'result': result
            }
        )


# Представление для обработки результатов запросов
class ResultViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()


# Представление для обработки истории запросов пользователя
class HistoryViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = QuerySerializer
    queryset = Query.objects.all()
    filterset_fields = ['kadastr_number', ]


# Представление для обработки запросов пользователя
class PingView(APIView):

    def get(self, request):
        debug = settings.DEBUG

        if debug:
            return Response(f'Сервер запущен в режиме разработки.')
        else:
            return Response('Сервер запущен в режиме продакшн.')


# Представление для стартовой страницы
def index_view(request):

    return render(request, "index.html")
