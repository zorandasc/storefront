from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Collection, Order, OrderItem, Product, Customer


# Create your views here.
def say_hello(request):
    #Every model has atribute objects
    #which return menager, interface to database
    #queryset=Product.objects.all()

    #queryset=Product.objects.filter(title__icontains='coffee')
    #queryset=Customer.objects.filter(email__icontains='.com')
    #queryset=Collection.objects.filter(featured_product__isnull=True)
    #queryset=Product.objects.filter(inventory__lt=10)
    #queryset=Order.objects.filter(customer__id=1)
    #queryset=OrderItem.objects.filter(product__collection__id=3)
    #and operater
    #queryset=Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    #or operater, negaet ~Q
    #queryset=Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    #query by field
    #queryset=Product.objects.filter(inventory=F('unit_price'))

    #sorting
    #queryset=Product.objects.order_by('title')
    #queryset=Product.objects.order_by('-title')

    #actual object 1
    #product=Product.objects.order_by('title')[0]

    #drugi nacin 2
    #product=Product.objects.earliest('unit_price')

    #limiting
    #queryset=Product.objects.all()[:5]

    #select only some fields to return
    #this return dictonary objects
    #queryset=Product.objects.values('title','id','collection__title')

    #returns tuples
    #queryset=Product.objects.values_list('title','id','collection__title')

    #product that have been ordered
    #queryset_first=OrderItem.objects.values('product_id').distinct()
    #queryset=Product.objects.filter(id__in=queryset_first)

    #with only dobijmao instance product classe
    #only method moze da bude opasana jer moze da generise dodatne querije
    #ako ne postiji value u prvom orginalnom queriju
    #toga nema kod values
    #queryset=Product.objects.only('id','title')

    #preload, django create join query 
    #select_reletaed when one relationship, npr> product ima jedan collection
    # ali mnogo promtionsa
    #queryset=Product.objects.select_related('collection').all()
    #queryset=Product.objects.prefetch_related('promotions').all()

    #queryset=Product.objects.prefetch_related('promotions').select_related('collection').all()

    #get the last 5 prders with their customer and items(incl product)
    #first query, Order.objects.select_related('customer'), inner join
    #second query, .prefetch_related('orderitem_set
    #third query,  .prefetch_related('orderitem_set__product')  
    queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


    #fUNC FOR CALLING DATABSES FUNCTIONS
    return render(request, 'hello.html', {'name': 'Mosh','products':list(queryset)})
