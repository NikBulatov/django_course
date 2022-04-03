from django.db import models


# Create your models of DB here

# Таблица в SQL (id сам создастся)
class ProductCategories(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=240, unique=True, null=False)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)  # 1:N

    def __str__(self):
        return f'{self.name} | {self.category}'
