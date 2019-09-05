from rest_framework_mongoengine import serializers
from . import models


class UserSerializer(serializers.DocumentSerializer):

    class Meta:
        #fields = ('eid', 'ename', 'email', 'econtact',)
        model = models.Employee
        fields = '__all__'
