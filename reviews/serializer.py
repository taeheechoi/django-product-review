from rest_flex_fields import FlexFieldsModelSerializer
from .models import Product, Category
from rest_framework import serializers

class CategorySerializer(FlexFieldsModelSerializer):
    
    class Meta:
        model = Category
        fields = ['pk', 'name']


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'content', 'created', 'updated']
        # fields = '__all__' 
        # exclude = ['category']
        # read_only_fields = ['name']
        # extra_kwargs = {'name': {'read_only': True}} 

        expandable_fields = {
            'category': (CategorySerializer, {'many': True})
        }


# class ProductSerializer(FlexFieldsModelSerializer):
#     category = CategorySerializer(many=True)

#     class Meta:
#         model = Product
#         fields = ['pk', 'name', 'category']
#         # fields = '__all__' 
#         # exclude = ['category']
#         # read_only_fields = ['name']
#         # extra_kwargs = {'name': {'read_only': True}} 

#         expandable_fields = {
#             'category': (CategorySerializer, {'many', True})
#         }
