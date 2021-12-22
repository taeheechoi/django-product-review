from django.contrib.auth.models import User
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import (Category, Comment, Company, Image, Product, ProductSite,
                     ProductSize)


class CompanySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'name', 'url']


class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']
        expandable_fields = {
          'products': ('reviews.ProductSerializer', {'many': True})
        }


class ProductSizeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['pk', 'name']


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'content', 'created', 'updated']
        expandable_fields = {
            'category': ('reviews.CategorySerializer', {'many': True}),
            'sites': ('reviews.ProductSiteSerializer', {'many': True}),
            'comments': ('reviews.CommentSerializer', {'many': True}),
            'image': ('reviews.ImageSerializer', {'many': True}),
        }


class ProductSiteSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSite
        fields = ['pk', 'name', 'price', 'url', 'created', 'updated']
        expandable_fields = {
            'product': 'reviews.CategorySerializer',
            'productsize': 'reviews.ProductSizeSerializer',
            'company': 'reviews.CompanySerializer',
        }


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'title', 'content', 'created', 'updated']
        expandable_fields = {
            'product': 'reviews.CategorySerializer',
            'user': 'reviews.UserSerializer'
        }


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='product_headshot'
        # sizes=[
        #     ('full_size', 'url'),
        #     ('thumbnail', 'thumbnail__100x100'), #  first position as the attribute of the image, second position as a ‘Rendition Key’ which dictates how the original image should be modified.
        # ]
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']

