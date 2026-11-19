from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .forms import ProductoForm
from .models import Producto


class ProductoCrudTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("tester", password="clave-segura-123")
        self.producto = Producto.objects.create(
            nombre="Teclado", descripcion="Mecánico", precio="29990.00", stock=5,
            propietario=self.user,
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



class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ana", password="clave-segura-123")

    def test_login_valido(self):
        resp = self.client.post(reverse("login"), {"username": "ana", "password": "clave-segura-123"})
        self.assertRedirects(resp, reverse("producto_list"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_invalido(self):
        resp = self.client.post(reverse("login"), {"username": "ana", "password": "incorrecta"})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_por_get_no_permitido(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_por_post_cierra_sesion(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_sin_csrf_es_rechazado(self):
        c = Client(enforce_csrf_checks=True)
        c.force_login(self.user)
        self.assertEqual(c.post(reverse("logout")).status_code, 403)
        self.assertIn("_auth_user_id", c.session)


class AccesoYPermisosTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.ana = User.objects.create_user("ana", password="clave-segura-123")
        self.beto = User.objects.create_user("beto", password="clave-segura-123")
        self.admin = User.objects.create_user("admin", password="clave-segura-123", is_staff=True)
        self.p_ana = Producto.objects.create(
            nombre="Producto de Ana", descripcion="x", precio="1000", stock=1, propietario=self.ana
        )
        self.datos = {"nombre": "Nuevo", "descripcion": "x", "precio": "1000", "stock": 1}

    def test_anonimo_no_accede_a_rutas_privadas(self):
        rutas = [
            reverse("producto_list"), reverse("producto_create"),
            reverse("producto_detail", args=[self.p_ana.pk]),
            reverse("producto_update", args=[self.p_ana.pk]),
            reverse("producto_delete", args=[self.p_ana.pk]),
        ]
        for url in rutas:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 302)
                self.assertTrue(resp.url.startswith("/login/"))

    def test_anonimo_no_puede_escribir(self):
        self.client.post(reverse("producto_create"), self.datos)
        self.client.post(reverse("producto_update", args=[self.p_ana.pk]), {**self.datos, "nombre": "Hackeado"})
        self.client.post(reverse("producto_delete", args=[self.p_ana.pk]))
        self.assertEqual(Producto.objects.count(), 1)
        self.p_ana.refresh_from_db()
        self.assertEqual(self.p_ana.nombre, "Producto de Ana")

    def test_otro_usuario_no_ve_el_detalle_ajeno(self):
        self.client.force_login(self.beto)
        resp = self.client.get(reverse("producto_detail", args=[self.p_ana.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_la_lista_solo_muestra_los_propios(self):
        self.client.force_login(self.beto)
        self.assertNotContains(self.client.get(reverse("producto_list")), "Producto de Ana")

    def test_otro_usuario_no_edita_ni_elimina(self):
        self.client.force_login(self.beto)
        r1 = self.client.post(reverse("producto_update", args=[self.p_ana.pk]), {**self.datos, "nombre": "Hackeado"})
        r2 = self.client.post(reverse("producto_delete", args=[self.p_ana.pk]))
        self.assertEqual((r1.status_code, r2.status_code), (404, 404))
        self.p_ana.refresh_from_db()
        self.assertEqual(self.p_ana.nombre, "Producto de Ana")

    def test_crear_asigna_el_propietario(self):
        self.client.force_login(self.beto)
        self.client.post(reverse("producto_create"), self.datos)
        self.assertEqual(Producto.objects.get(nombre="Nuevo").propietario, self.beto)

    def test_el_dueno_edita_y_elimina_lo_suyo(self):
        self.client.force_login(self.ana)
        self.client.post(reverse("producto_update", args=[self.p_ana.pk]), {**self.datos, "nombre": "Editado"})
        self.p_ana.refresh_from_db()
        self.assertEqual(self.p_ana.nombre, "Editado")
        self.client.post(reverse("producto_delete", args=[self.p_ana.pk]))
        self.assertFalse(Producto.objects.filter(pk=self.p_ana.pk).exists())

    def test_el_personal_ve_todos(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("producto_list")), "Producto de Ana")