from django.contrib import admin

from product.models import Variation

# Register your models here.

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ("name",)