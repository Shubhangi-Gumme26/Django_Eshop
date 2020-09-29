from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.order import Order
from .models.customer import Customer
from .models.product import Subcategory, Category, ProductColor, ProductBrand, ProductSize, Product


# Register your models here.
class CategoryAdmin(ModelAdmin):
    list_display = ["category_name"]
    search_fields = ["category_name"]
    list_filter = ["category_name"]
admin.site.register(Category, CategoryAdmin)

class SubcategoryAdmin(ModelAdmin):
    list_display = ["subcategory_name", "category_name", ]
    search_fields = ["category_name", "subcategory_name"]
    list_filter = ["category_name"]
admin.site.register(Subcategory, SubcategoryAdmin)

class ProductSizeAdmin(ModelAdmin):
    list_display = ["product_size"]
    search_fields = ["product_size"]
    list_filter = ["product_size"]
admin.site.register(ProductSize, ProductSizeAdmin)

class ProductBrandAdmin(ModelAdmin):
    list_display = ["product_brand"]
    search_fields = ["product_brand"]
    list_filter = ["product_brand"]
admin.site.register(ProductBrand, ProductBrandAdmin)

class ProductColorAdmin(ModelAdmin):
    list_display = ["product_color"]
    search_fields = ["product_color"]
    list_filter = ["product_color"]
admin.site.register(ProductColor, ProductColorAdmin)

class ProductAdmin(ModelAdmin):
    list_display = ["product_name", "category_name", "subcategory_name", "product_sell_price", "product_color", "product_size", "product_available", "product_created_date"]
    search_fields = ["product_name", "product_description", "category_name", "subcategory_name", "product_brand", "product_color", "product_size"]
    list_filter = ["category_name", "product_brand", "product_color", "product_size", "product_available"]
admin.site.register(Product, ProductAdmin)

class CustomerAdmin(ModelAdmin):
    list_display = ["name", "phone", "email"]
    search_fields = ["name", "email", "phone"]
    list_filter = ["email", "phone"]
admin.site.register(Customer, CustomerAdmin)

class OrderAdmin(ModelAdmin):
    list_display = ["customer", "product", "quantity", "price", "address", "ordered_date"]
    search_fields = ["address", "customer", "phone"]
    list_filter = ["status", "customer"]
admin.site.register(Order, OrderAdmin)