from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductoForm
from .models import Producto


class PropietarioQuerysetMixin:
    """Cada usuario ve solo sus productos; el personal (is_staff) ve todos."""

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(propietario=self.request.user)


class ProductoListView(LoginRequiredMixin, PropietarioQuerysetMixin, ListView):
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "productos"
    ordering = ["nombre"]
    queryset = Producto.objects.prefetch_related("skills")


class ProductoDetailView(LoginRequiredMixin, PropietarioQuerysetMixin, DetailView):
    model = Producto
    template_name = "productos/producto_detail.html"
    context_object_name = "producto"


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("producto_list")

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, PropietarioQuerysetMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("producto_list")


class ProductoDeleteView(LoginRequiredMixin, PropietarioQuerysetMixin, DeleteView):
    model = Producto
    template_name = "productos/producto_confirm_delete.html"
    success_url = reverse_lazy("producto_list")