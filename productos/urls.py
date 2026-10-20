from django.urls import path

from .views import (
    ProductoListView,
    ProductoDetailView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView
)


urlpatterns = [

    path(
        '',
        ProductoListView.as_view(),
        name='producto_list'
    ),

    path(
        'producto/<int:pk>/',
        ProductoDetailView.as_view(),
        name='producto_detail'
    ),

    path(
        'nuevo/',
        ProductoCreateView.as_view(),
        name='producto_create'
    ),

    path(
        'editar/<int:pk>/',
        ProductoUpdateView.as_view(),
        name='producto_update'
    ),

    path(
        'eliminar/<int:pk>/',
        ProductoDeleteView.as_view(),
        name='producto_delete'
    ),

]