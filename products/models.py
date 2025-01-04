from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.auth.models import User



# Category model
class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
    
# SubCategory model
class SubCategory(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL, related_name="subcategories")
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('SubCategory', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True, storage=MediaCloudinaryStorage())

    def save(self, *args, **kwargs):
        if self.image:
            self.image_url = self.image.url  # Automatically set the Cloudinary URL
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i} - {rating}") for i, rating in enumerate(["Very Bad", "Bad", "Average", "Good", "Excellent"], 1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    
class JewelryCustomization(models.Model):
    MATERIAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    ]

    GEMSTONE_CHOICES = [
        ('diamond', 'Diamond'),
        ('ruby', 'Ruby'),
        ('sapphire', 'Sapphire'),
        ('emerald', 'Emerald'),
        ('pearl', 'Pearl'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customizations')
    jewelry_item = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='customizations')  # Assuming you have a 'Product' model
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='gold')
    gemstone = models.CharField(max_length=20, choices=GEMSTONE_CHOICES, default='diamond', blank=True, null=True)
    engraving_text = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=10)  # Could be 'Small', 'Medium', 'Large', or numeric size like ring sizes
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Custom price depending on customization
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customization for {self.jewelry_item.name} by {self.user.username}"
