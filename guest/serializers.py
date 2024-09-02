from rest_framework import serializers
from guest.models import *

class employeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'