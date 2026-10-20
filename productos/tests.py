from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProductoForm
from .models import Producto


class ProductoCrudTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("tester", password="clave-segura-123")
        self.producto = Producto.objects.create(
            nombre="Teclado", descripcion="Mecánico", precio="29990.00", stock=5
        )

    def test_requiere_login(self):
        resp = self.client.get(reverse("producto_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_listar(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("producto_list"))
        self.assertContains(resp, "Teclado")

    def test_ver_detalle_producto(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("producto_detail", args=[self.producto.pk])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Teclado")
        self.assertContains(resp, "Mecánico")

    def test_crear(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("producto_create"),
            {"nombre": "Mouse", "descripcion": "Óptico", "precio": "9990", "stock": 10},
        )
        self.assertRedirects(resp, reverse("producto_list"))
        self.assertTrue(Producto.objects.filter(nombre="Mouse").exists())

    def test_editar(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("producto_update", args=[self.producto.pk]),
            {"nombre": "Teclado RGB", "descripcion": "Mecánico", "precio": "34990", "stock": 3},
        )
        self.assertRedirects(resp, reverse("producto_list"))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Teclado RGB")

    def test_eliminar(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse("producto_delete", args=[self.producto.pk]))
        self.assertRedirects(resp, reverse("producto_list"))
        self.assertFalse(Producto.objects.exists())

    def test_rechaza_valores_negativos(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("producto_create"),
            {"nombre": "X", "descripcion": "Y", "precio": "-1", "stock": -5},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Producto.objects.count(), 1)

    def test_login_renderiza(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)


# --- Validación en el servidor (Unidad 2) -----------------------------------

BASE = {"nombre": "Mouse", "descripcion": "Óptico", "precio": "9990", "stock": 10}


class ProductoFormValidacionTests(TestCase):
    """Valida el formulario directamente, sin navegador."""

    def test_casos_nombre_y_stock(self):
        casos = [
            ("nombre", "Mouse", True),
            ("nombre", "", False),
            ("nombre", "ab", False),
            ("nombre", "abc", True),
            ("nombre", "a" * 100, True),
            ("nombre", "a" * 101, False),
            ("stock", 10, True),
            ("stock", -1, False),
            ("stock", 0, True),
            ("stock", 100000, True),
            ("stock", 100001, False),
        ]
        for campo, valor, valido in casos:
            with self.subTest(campo=campo, valor=str(valor)[:10]):
                form = ProductoForm(data={**BASE, campo: valor})
                self.assertEqual(form.is_valid(), valido, form.errors.as_json())


class ProductoVistaValidacionTests(TestCase):
    """La vista no guarda datos inválidos aunque se salte el HTML."""

    def setUp(self):
        self.user = get_user_model().objects.create_user("tester", password="clave-segura-123")
        self.client.force_login(self.user)

    def test_vista_rechaza_stock_sobre_el_maximo(self):
        resp = self.client.post(reverse("producto_create"), {**BASE, "stock": 100001})
        self.assertEqual(resp.status_code, 200)  # vuelve al formulario con errores
        self.assertEqual(Producto.objects.count(), 0)