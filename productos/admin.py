from django.contrib import admin

from .models import Producto, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock")
    search_fields = ("nombre", "descripcion")
    filter_horizontal = ("skills",)
