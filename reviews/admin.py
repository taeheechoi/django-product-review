from django.contrib import admin
from .models import Product, Category, Company, ProductSize, ProductSite, Comment, Image
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'content')
    list_filter = ('category', )

admin.site.site_header = 'Product Review Admin'
# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(ProductSize)
admin.site.register(ProductSite)
admin.site.register(Comment)
admin.site.register(Image)

admin.site.unregister(Group)






















