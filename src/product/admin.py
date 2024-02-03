from django.contrib import admin
from .models import Product, ProductVariant, ProductVariantPrice, Variant, ProductImage

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "sku", "description"]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(ProductVariantPrice)
class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "file_path"]
