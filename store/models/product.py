from django.db import models
from django.db.models import CASCADE



# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.category_name

    @staticmethod  # fatch all categories
    def all_categories():
        return Category.objects.all()




class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=200)
    category_name = models.ForeignKey(to="Category", on_delete=CASCADE)
    class Meta:
        verbose_name_plural = "Subategories"
    def __str__(self):
        return self.subcategory_name




class ProductSize(models.Model):
    product_size = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "ProductSizes"
    def __str__(self):
        return self.product_size




class ProductBrand(models.Model):
    product_brand = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "ProductBrands"
    def __str__(self):
        return self.product_brand




class ProductColor(models.Model):
    product_color = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "ProductColors"
    def __str__(self):
        return self.product_color




class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(default="", blank=False, null=False)
    product_created_date = models.DateTimeField(auto_now_add=True)
    product_updated_date = models.DateTimeField(auto_now_add=True)
    product_sell_price = models.IntegerField(default=0, blank=False, null=False)
    product_image = models.ImageField(upload_to="store/images/")
    category_name = models.ForeignKey(to="Category", on_delete=CASCADE)
    subcategory_name = models.ForeignKey(to="Subcategory", on_delete=CASCADE)
    product_brand = models.ForeignKey(to="ProductBrand", on_delete=CASCADE)
    product_color = models.ForeignKey(to="ProductColor", on_delete=CASCADE)
    product_size = models.ForeignKey(to="ProductSize", on_delete=CASCADE)
    product_available = models.BooleanField(default=True)
    class Meta:
        ordering = ['-product_created_date']
    def __str__(self):
        return self.product_name

    @staticmethod                 # fatch all products
    def all_products():
        return Product.objects.all()

    @staticmethod
    def get_products_by_id(ids):                     #get all products by id
        return Product.objects.filter(id__in=ids)

    @staticmethod                           # get individual category related products from database
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category_name=category_id)
        else:
            return Product.all_products();

