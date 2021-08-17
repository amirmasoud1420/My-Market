from rest_framework import serializers
from .models import *
from .api_views import *
from core.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ['password']


# User Short Serializer
class UserShortSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'password']


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user_detail_api', read_only=True)
    addresses = serializers.HyperlinkedRelatedField(view_name='address_detail_api', read_only=True,
                                                    many=True, source='address_set')
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = '__all__'


# Customer Short Serializer
class CustomerShortSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user_detail_api', queryset=User.objects.all())
    addresses = serializers.HyperlinkedRelatedField(view_name='address_detail_api', queryset=Address.objects.all(),
                                                    many=True, source='address_set')

    class Meta:
        model = Customer
        fields = ['id', 'user', 'image', 'addresses']


# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='customer_detail_api', read_only=True)
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Address
        fields = '__all__'


# Address Short Serializer
class AddressShortSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='customer_detail_api', queryset=Customer.objects.all())

    class Meta:
        model = Address
        fields = ['id', 'owner', 'state', 'city', 'postal_code', 'detail', 'lat', 'lng']
