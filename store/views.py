import jwt
from django.shortcuts import render
from django.conf import settings
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK

from .models import (Collection, Product, Plan,
                     Customer)
from .serializers import (CollectionSerializer, ProductSerializer, PlanSerializer,
                        UserProfileSerializer, CustomerProfileSerializer)
from .permissions import (IsAdminOrReadOnly)
from .filters import PlanFilter, ProductFilter
from .pagination import DefaultPagination


class PlanViewSet(ModelViewSet):
    http_method_names = ['get', 'option', 'head']

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PlanFilter
    ordering_fields = ['unit_price']    
    pagination_class = DefaultPagination


class ProductViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter

    def destroy(self, request, *args, **kwargs):
        if Plan.objects.filter(associates_product_id=kwargs['pk']).count() > 0:
            return Response(
                {'errors': 'Product cannot be deleted because it is  \
                 associated with one or more plans'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) 
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']

    queryset = Collection.objects.annotate(
        products_count=Count("products")
    ).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {'errors': 'Collection cannot be deleted because it is  \
                 associated with one or more products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) 
        return super().destroy(request, *args, **kwargs)
        

class UserProfileViewSet(ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    '''
        host/users/me
        url to change user credentials
    '''
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserProfileSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)


class CustomerProfileViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAdminUser]
    '''
        host/customers/me
        show case user info and wallet
    '''
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerProfileSerializer(customer)
            return Response(serializer.data)
        
