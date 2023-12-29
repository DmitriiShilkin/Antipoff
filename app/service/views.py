import sys

from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Query, Result
from .serializers import QuerySerializer, ResultSerializer


# Представления для обработки запросов пользователя
class QueryViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = QuerySerializer
    queryset = Query.objects.all()

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            serializer.save()
            message = 'True'
            Result.objects.create(
                message=message,
                query=Query.objects.get(id=serializer.data['id'])
            )
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': message,
                }
            )

        message = 'False'

        if status.HTTP_400_BAD_REQUEST:
            Result.objects.create(
                message=serializer.errors,
                kadastr_number=serializer.data['kadastr_number'],
                latitude=serializer.data['latitude'],
                longitude=serializer.data['longitude']
            )
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': message,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            Result.objects.create(
                message='Internal Server Error',
                kadastr_number=serializer.data['kadastr_number'],
                latitude=serializer.data['latitude'],
                longitude=serializer.data['longitude']
            )
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': message,
                }
            )


# Представления для обработки результатов запросов
class ResultViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()


# Представления для обработки истории запросов пользователя
class HistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuerySerializer
    queryset = Query.objects.all().order_by('-created')
    filterset_fields = ['kadastr_number', ]


# Представление для обработки запросов пользователя
class PingView(APIView):

    def get(self, request):
        debug = settings.DEBUG

        if debug:
            return Response(f'Сервер запущен в режиме разработки.')
        else:
            return Response('Сервер запущен в режиме продакшн.')


# Представление-заглушка для стартовой страницы
def index_view(request):

    return render(request, "index.html")
