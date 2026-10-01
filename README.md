# proyecto_crud

CRUD de productos hecho con Django, con autenticación y estilos con Tailwind.

## Puesta en marcha

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # y edita los valores (SECRET_KEY, etc.)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego entra a http://127.0.0.1:8000/ e inicia sesión.

## Tests

```bash
python manage.py test
```

## Rutas

| Ruta | Descripción |
|------|-------------|
| `/` | Lista de productos |
| `/nuevo/` | Crear producto |
| `/editar/<id>/` | Editar producto |
| `/eliminar/<id>/` | Eliminar producto |
| `/login/`, `/logout/` | Autenticación |
| `/admin/` | Panel de administración |
