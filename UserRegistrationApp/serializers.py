from rest_framework import serializers
from .models import User
#from rest_auth.registration.serializers import RegisterSerializer


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name','height' )

