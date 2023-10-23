from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (Collection, Product, Plan,
                     Customer)


class SimpleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title']

class SimpleAssociatesProductSerializer(serializers.ModelSerializer):
    collection = SimpleCollectionSerializer()
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'collection']

class PlanSerializer(serializers.ModelSerializer):
    associated_product = SimpleAssociatesProductSerializer()

    class Meta:
        model = Plan
        fields = ['title', 'unit_price', 'description', 'associated_product']


class SimpleFeaturedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']

class CollectionSerializer(serializers.ModelSerializer):
    featured_product = SimpleFeaturedProductSerializer()
    
    class Meta:
        model = Collection
        fields = ['id' ,'title', 'products_count', 'featured_product']

    products_count = serializers.IntegerField()


class SimpleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title']

class ProductSerializer(serializers.ModelSerializer):
    collection = SimpleCollectionSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'collection']


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    class Meta:
        User = get_user_model()
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    wallet = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['wallet', 'user']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name']


