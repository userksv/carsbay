from django.contrib import admin
from main.models import Post, PostImage, Brand, CarModel, City

# # Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(City)
