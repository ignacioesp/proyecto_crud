# proyecto_crud

CRUD de productos hecho con Django, con login, permisos por propietario y estilos con Tailwind.
Esta versión se ejecuta en Docker Compose y se analiza con OWASP ZAP en un laboratorio local, con datos ficticios.

## Requisitos
- Docker Desktop con Docker Compose (en Windows, con WSL 2)
- Python 3.13 y Git (solo para ejecutar sin Docker)

## Ejecución con Docker (laboratorio)
```bash
cp .env.docker.example .env.docker     # Windows (PowerShell): Copy-Item .env.docker.example .env.docker
# Edita .env.docker y reemplaza SECRET_KEY por una clave larga y aleatoria. No la subas al repositorio.
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
```
El servicio queda publicado solo en la interfaz local: http://127.0.0.1:8000

## Cuentas de prueba (ficticias)
```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model as g; g().objects.create_user('usuario1', password='<clave-de-prueba>')"
```
Cada usuario solo ve, edita y elimina sus productos. El personal (is_staff) ve todos.

## Detener y limpiar
```bash
docker compose down            # detiene el servicio
docker compose down -v         # además borra el volumen con la base de datos de prueba
```

## Pruebas
```bash
docker compose exec web python manage.py test productos
```

## Ejecución local sin Docker
```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # y edita los valores
python manage.py migrate
python manage.py runserver
```

## Seguridad del laboratorio
- No subir .env, .env.docker, claves, tokens ni bases de datos al repositorio.
- Usar solo cuentas y datos ficticios. No escanear despliegues públicos ni sitios de terceros.
- Perfil de laboratorio: DEBUG=False, ALLOWED_HOSTS acotado y secretos por variables de entorno.