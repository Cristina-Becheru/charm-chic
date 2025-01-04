from django.contrib import admin
from .models import Product, Category, SubCategory, Tag, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'sku',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'category',
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')  
    list_filter = ('product', 'user', 'rating')  
    search_fields = ('user__username', 'product__name', 'comment')  

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Tag)
admin.site.register(Review, ReviewAdmin) 