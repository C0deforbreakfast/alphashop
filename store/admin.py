from typing import Any, Optional

from django.contrib import admin
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode

from django.db.models.query import QuerySet
from django.db.models.aggregates import Count, Sum
from django.db.models import Value

from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from .models import (Collection, Product, Plan,
                     Customer, Order, OrderItem)


class PlanInLineNested(NestedTabularInline):
    model = Plan
    extra = 1
    fk_name = 'associated_product'

class ProductInLineNested(NestedTabularInline):
    model = Product
    min_num = 0
    max_num = 90
    extra = 1
    fk_name = 'collection'
    inlines = [PlanInLineNested]

    prepopulated_fields = {
        'slug': ['title']
    }
    fields = ('title', 'description', 'slug')
    
@admin.register(Collection)
class CollectionAdmin(NestedModelAdmin):
    list_display = ['id', 'title', 'products_count', 'products_link']
    list_display_links = ['title']
    search_fields = ['title']
    fields = ('title',)
    inlines = [ProductInLineNested]

    def products_link (self, collection):
        # For getting url to products of each collection
        print(collection.id)
        url = (reverse('admin:store_product_changelist')
                # To make string queries
                + '?'
                # To only show the prodcuts in the specified collection
                + urlencode({
                    'collection__id': str(collection.id),
                }))
        # Creating an html snippet in admin interface
        return format_html('<a href="{}">{}</a>', url, collection.products_link)

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('products'),
            products_link=Value('See all products')
        )


class PlanInLine(admin.TabularInline):
    model = Plan
    min_num = 0
    max_num = 90
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {
        'slug': ['title']
    }

    fields = ('title', 'description', 'slug', 'collection')
    autocomplete_fields = ['collection']
    list_display = ['id', 'title', 'description', 'last_updated', 'collection_title',
                    'plans_count', 'plans_link']
    list_display_links = ['title']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    inlines = [PlanInLine]

    def plans_link (self, product):
        print(product.id)
        url = (reverse('admin:store_plan_changelist')
                + '?'
                + urlencode({
                    'associated_product__id': str(product.id),
                }))
        return format_html('<a href="{}">{}</a>', url, product.plans_link)

    def plans_count(self, product):
        return product.plans_count

    def collection_title(self, product):
        return product.collection.title

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            plans_count=Count('plans'), plans_link=Value('See all plans')
        )

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'associated_product_title', 'unit_price']
    list_filter = ['associated_product']
    list_select_related = ['associated_product']
    list_editable = ['unit_price']
    list_per_page = 10
    search_fields = ['associated_product__title']

    @admin.display(ordering='associated_product_title')
    def associated_product_title(self, plan):
        return plan.associated_product.title
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request) \
            .prefetch_related('associated_product')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    fields = ('membership', 'wallet', 'user')
    list_display = ['first_name', 'last_name', 'membership',
                    'wallet', 'phone_number', 'user_email']
    search_fields = ['membership', 'user__first_name', 'user__last_name']
    list_select_related = ['user']
    list_per_page = 10
    list_filter = ['membership']

    def user_email(self, customer):
        return customer.user.email

    

'''Show associated data'''
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     display_fields = ['product', 'order', 'associated_plans']

#     def associated_plan(self, orderitem):
#         associated_plans = Plan.objects.filter(
#             associated_product_id=orderitem.product_id)
#         return associated_plans

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    autocomplete_fields = ['plan']
    fields = ('product', 'plan')

    min_num = 1
    max_num = 90
    extra = 0

    def item_price(self, orderitem):
        return orderitem.plan.unit_price

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'placed_at', 'payment_status', 'total_price']
    list_display_links = ['customer']
    list_filter = ['payment_status']
    # search_fields = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    def total_price(self, order):
        queryset = OrderItem.objects \
            .prefetch_related('plan') \
            .filter(order_id=order.id)
        
        price_sum = 0
        for query in queryset:
            price_sum += query.plan.unit_price
        query.unit_price = price_sum

        return query.unit_price
