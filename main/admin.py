from django.contrib import admin
from main.models import Post, PostImage, Brand, CarModel, City

# # Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(City)

# class ImageAdmin(admin.StackedInline):
#     model = Image

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [ImageAdmin]

#     class Meta:
#        model = Post

# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     pass
