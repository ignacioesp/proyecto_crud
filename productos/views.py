from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import ProductoForm
from .models import Producto


class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "productos"
    ordering = ["nombre"]


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("producto_list")


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("producto_list")


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/producto_confirm_delete.html"
    success_url = reverse_lazy("producto_list")
