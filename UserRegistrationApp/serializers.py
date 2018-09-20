from rest_framework import serializers
from .models import Json1Test


class Json1TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Json1Test
        fields = ('id', 'name', 'email', 'date', 'subject', 'description')
