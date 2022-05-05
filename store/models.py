from msilib.schema import Class
from django.db import models

# Create your models here.
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)
    #sad imamo circular dependency izmedju collection i products
    #zato koristimo navodnike, i posto nas ne zanima reverse polje u Product
    #klasi stavljamo related_name='+'
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=6, decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    #one to many
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    #many to many
    promotions=models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'

    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]

    first_name=models.CharField(max_length=255)
    slug=models.SlugField(default='-')
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    class Meta:
        indexes=[
            models.Index(fields=['last_name','first_name'])
        ]

class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    #primary key na customeru omogucuje one to one relationship
    #reverese polje address on custemer will be automatyick set
    #customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    #zip=models.IntegerField()

class Order(models.Model):
        PAYMENT_STATUS_PENDING='P'
        PAYMENT_STATUS_COMPLETE='C'
        PAYMENT_STATUS_FAILED='F'

        PAYMENT_STATUS_CHIOCES=[
            (PAYMENT_STATUS_PENDING,'Pending'),
            (PAYMENT_STATUS_COMPLETE, 'Complete'),
            (PAYMENT_STATUS_FAILED,'Failed')
        ]
        
        placed_at=models.DateTimeField(auto_now_add=True)
        payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS_CHIOCES,default=PAYMENT_STATUS_PENDING)
        customer=models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()




















































