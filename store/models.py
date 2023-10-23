from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)
                                               ])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',
                                        on_delete=models.SET_NULL, 
                                        related_name='+',
                                        null=True,)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    last_updated = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection,
                                on_delete=models.PROTECT,
                                related_name='products')
    plan = models.ForeignKey('Plan',
                            on_delete=models.SET_NULL,
                            related_name='product',
                            null=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['title']


class Plan(models.Model):
    title = models.CharField(max_length=255)
    unit_price = models.BigIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    associated_product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name='plans')

    '''Show associated data'''
    def __str__(self):
        return f"{self.title}-{self.associated_product.title} {self.unit_price}"
    

    class Meta:
        ordering = ['unit_price', 'associated_product']


class Customer(models.Model):
    MEMBERSHIP_SIMPLE = 'Simple'
    MEMBERSHIP_VIP = 'VIP'
    MEMBERSHIP_ADMIN = 'Admin'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_SIMPLE, 'Simple'),
        (MEMBERSHIP_VIP, 'VIP'),
        (MEMBERSHIP_ADMIN, 'Admin')
    ]
    
    membership = models.CharField(
        verbose_name=_('Membership'),
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_SIMPLE,
    )
    wallet = models.BigIntegerField(default=0)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__phone_number')
    def phone_number(self):
        return self.user.phone_number
    
    # class Meta:
    #     ordering = ['membership']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='cartitems')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, 
                                      choices=PAYMENT_STATUS_CHOICES, 
                                      default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT,
                              related_name='items')
    product = models.ForeignKey(Product, 
                                on_delete=models.PROTECT, 
                                related_name='orderitems')
    plan = models.ForeignKey(Plan,
                             on_delete=models.PROTECT,
                             related_name='orderplans')
    unit_price = models.BigIntegerField(validators=[MinValueValidator(0)],
                                        default=0)