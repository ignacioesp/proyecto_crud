from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Producto


class ProductoListView(LoginRequiredMixin, ListView):

    model = Producto

    template_name = 'productos/producto_list.html'

    context_object_name = 'productos'


class ProductoCreateView(LoginRequiredMixin, CreateView):

    model = Producto

    template_name = 'productos/producto_form.html'

    fields = [
        'nombre',
        'descripcion',
        'precio',
        'stock'
    ]

    success_url = reverse_lazy('producto_lista')


class ProductoUpdateView(LoginRequiredMixin, UpdateView):

    model = Producto

    template_name = 'productos/producto_form.html'

    fields = [
        'nombre',
        'descripcion',
        'precio',
        'stock'
    ]

    success_url = reverse_lazy('producto_lista')


class ProductoDeleteView(LoginRequiredMixin, DeleteView):

    model = Producto

    template_name = 'productos/producto_confirm_delete.html'

    success_url = reverse_lazy('producto_lista')