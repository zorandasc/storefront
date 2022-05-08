from django.contrib import admin
from django.http import HttpRequest
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode

from store.models import Collection, Customer, Order, OrderItem, Product


class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'

    def lookups(self, request, model_admin):
        return [('<10','Low')]

    def queryset(self, request,queryset):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display=['title', 'unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=10
    #eager load this fields
    list_select_related=['collection']
    list_filter=['collection', 'last_update', InventoryFilter]
    actions=['clear_inventory']
    prepopulated_fields={'slug':['title']}
    autocomplete_fields=['collection']
    search_fields=['title']

    #computed column
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request,queryset):
        #queryset je ono sto je korisnik selekotovao
        #kvacicama
        updated_count=queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} sucesfule updated')

    def collection_title(self,product):
        return product.collection.title

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title']

    #collection je default queryset
    #posto u njemu nema products_count
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        #admin:app_model_page
        url=reverse('admin:store_product_changelist')+'?'+urlencode({'collection__id':str(collection.id)})
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        
    #modifukujemo mi da bi dobili polje product_count
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'membership','orders']
    list_editable=['membership']
    ordering=['first_name','last_name']
    list_per_page=10
    search_fields=['first_name__istartswith','last_name__istartswith']

    #collection je default queryset
    #posto u njemu nema products_count
    @admin.display(ordering='orders')
    def orders(self,customer):
        #admin:app_model_page
        url=reverse('admin:store_order_changelist')+'?'+urlencode({'customer__id':str(customer.id)})
        return format_html('<a href="{}">{} Orders</a>',url,customer.orders)
        
    #modifukujemo mi da bi dobili polje product_count
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields=['product']
    model=OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'placed_at', 'customer']
    autocomplete_fields=['customer']
    inlines=[OrderItemInline]









