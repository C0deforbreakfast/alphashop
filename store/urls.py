from django.urls import path, include
from rest_framework import routers

from .views import (CollectionViewSet, ProductViewSet, PlanViewSet,
                    UserProfileViewSet, CustomerProfileViewSet)

router = routers.DefaultRouter()
router.register('collections', CollectionViewSet, basename="collection")
router.register('products', ProductViewSet, basename="product")
router.register('plans', PlanViewSet, basename="Plan")
router.register('users', UserProfileViewSet, basename='User')
router.register('customers', CustomerProfileViewSet, basename='Customer')

urlpatterns = router.urls
