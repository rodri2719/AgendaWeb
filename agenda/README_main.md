# Explicación de `main.py`

Este archivo implementa una agenda web básica usando **web.py** y **SQLite**. Permite listar, agregar, ver detalles, editar y borrar personas en una base de datos.

## ¿Qué hace el código?
- Define rutas para cada acción (listar, insertar, detalle, editar, borrar).
- Cada ruta está asociada a una clase controladora que gestiona la lógica correspondiente.
- Usa plantillas HTML en la carpeta `templates/` para mostrar los datos y formularios.
- Se conecta a la base de datos `agenda.db` para realizar operaciones CRUD sobre la tabla `personas`.

## Estructura principal
- **Rutas:**
  - `/` → Lista todas las personas.
  - `/insertar` → Formulario para agregar una persona.
  - `/detalle/<id>` → Muestra los datos de una persona.
  - `/editar/<id>` → Permite editar los datos de una persona.
  - `/borrar/<id>` → Elimina una persona.
- **Controladores:**
  - `Index`: Muestra la lista de personas.
  - `Insertar`: Permite agregar una nueva persona.
  - `Detalle`: Muestra los datos de una persona específica.
  - `Editar`: Permite modificar los datos de una persona.
  - `Borrar`: Elimina una persona de la base de datos.
- **Base de datos:**
  - Usa `sqlite3` para conectarse y ejecutar consultas SQL.
- **Plantillas:**
  - Usa el motor de plantillas de web.py para renderizar las vistas HTML.

## Flujo básico
1. El usuario accede a la página principal (`/`) y ve la lista de personas.
2. Puede insertar una nueva persona desde `/insertar`.
3. Puede ver detalles, editar o borrar cada persona usando los enlaces correspondientes.
4. Todas las operaciones se reflejan en la base de datos SQLite.

## Notas
- El código incluye manejo básico de errores y mensajes para el usuario.
- La eliminación se realiza por GET para simplicidad, pero en producción debería hacerse por POST.

---
**Autor:** Rodri_7z
**Licencia:** MIT
