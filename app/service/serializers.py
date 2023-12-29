from rest_framework import serializers

from .models import Query, Result


# Сериализатор данных модели Query
class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = [
            'id',
            'created',
            'kadastr_number',
            'latitude',
            'longitude',
        ]


# Сериализатор данных модели Result
class ResultSerializer(serializers.ModelSerializer):
    query = QuerySerializer

    class Meta:
        model = Result
        depth = 1
        fields = [
            'id',
            'created',
            'message',
            'kadastr_number',
            'latitude',
            'longitude',
            'query',
        ]
