Tutorial from 
https://medium.com/django-rest/django-rest-framework-creating-views-and-serializers-b76a96fb6fb7

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install django djangorestframework markdown
$ django-admin startproject medium .
$ python manage.py startapp reviews
$ python manage.py migarte

reviews/modles.py

```
product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
```

related_name: the attribute of the related object that allows you to go ‘backwards’ to the model with the foreign key on it. 
product_instance.comments.all(), comment instances related to product instance

related_query_name : For Django querysets. It allows you to filter on the reverse relationship of a foreign key related field.
Product.objects.filter(comment=filter), comment as a lookup parameter in queryset

$ python manage.py makemigrations, to reflect changes on models, changes to be stored as a migration.
$ python manage.py migrate, synchronizing the changes of models with the schema in the database.

$ python manage.py createsuperuser
$ python manage.py runserver

reviews/admin.py, to see models on the admin panel
```
from django.contrib import admin
from .models import Product, Category, Company, ProductSize, ProductSite, Comment

admin.site.site_header = “Product Review Admin”
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'content') # many to many fields are not allowed
    list_filter = ('category', )


admin.site.register(Product)
...
admin.site.unregister(Group)
```

serializer:  querysets and model instances to be converted to native Python data types -> JSON, “translating” Django models into other formats
```
m django.core import serializers
data = serializers.serialize("xml", SomeModel.objects.all())
```
deserialization: JSON -> Python data types -> queryset or model instance

ModelSerializer class: Model fields to serializer + validators

Django validation: partially on the form and model instance
DRF validation: entirely on serializer class
1. Field level validation: validate_Field_Name
2. Object level validation: for multiple fields
3. Overriding serializer methods: create() or update() or both
```
def create(self, validated_data):
    return Comment.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.email = validated_data.get('email', instance.email)
    instance.title = validated_data.get('content', instance.title)
    instance.save()
    return instance
```
4. Including extra context: for what????
```
serializer = ProductSerializer(account, context={'request': request})
```
5. Nested relationships: nested relationships can be expressed by using serializers as fields
6. SerializerMethodField: value by calling a method on the serializer class

GenericViewSet: no get/post/put, get_object() and get_queryset() only

ViewSet: GenericViewSet + getting list of objects and detail of one object included. Router generates urls for Viewset automatically

ReadOnlyModelViewSet: list() and retrieve(), get only

ModelViewSet: create(), retrieve(), update(), partial_update(), destroy() and list()


```
from rest_framework.decorators import action

class ProductViewSet(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    @action(detail=False) # products/get_list GET
    def get_list(self, request):
        pass
      
    @action(detail=True) # products/get_product/:pk GET
    def get_product(self, request, pk=None):
        pass


    @action(detail=True, methods=['post', 'delete']) # products/delete_product/:pk DELETE POST
    def delete_product(self, request, pk=None):
        pass

```

FlexFields package for dynamic serialization.
$ pip install wheel
$ pip install drf-flex-fields
```
http://127.0.0.1:8000/product/
http://127.0.0.1:8000/product/?fields=pk,name
http://127.0.0.1:8000/product/?omit=content
http://127.0.0.1:8000/product/?expand=category
http://127.0.0.1:8000/product/1/?expand=category
http://127.0.0.1:8000/product/?expand=category&fields=name,category.name
http://127.0.0.1:8000/product/1/?expand=category,comments,sites.company,sites.productsize&omit=content
http://127.0.0.1:8000/product/?expand=category,comments,sites.company,sites.productsize&omit=content&category=4
http://127.0.0.1:8000/product/1/?expand=image&omit=content
```

To avoid circular import problems, it’s possible to lazily evaluate a string reference to you serializer class
```
expandable_fields = {
  'category': ('reviews.CategorySerializer', {'many': True})
}
``` 
```
class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'), #  first position as the attribute of the image, second position as a ‘Rendition Key’ which dictates how the original image should be modified.
        ]
    )

```

https://github.com/rsinger86/drf-flex-fields
https://www.test-cors.org/

CorsMiddleware should be placed before CommonMiddleware 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://www.test-cors.org",
]

CSRF_TRUSTED_ORIGINS = [
    'www.test-cors.org',
]

CORS_ALLOW_CREDENTIALS = True

Rotate the refresh tokens so that our users don’t have to log in again if they visit within 15 days.
SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
}