from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
