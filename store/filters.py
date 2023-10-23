from django_filters import FilterSet
from .models import Plan, Product


class PlanFilter(FilterSet):
    class Meta:
        model = Plan
        fields = {
            'unit_price': ['lt', 'gt'],
            'associated_product': ['exact'],
            'associated_product__collection': ['exact']
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection': ['exact'],
        }
