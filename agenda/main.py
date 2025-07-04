# Importa el módulo 'web' de web.py, que es un framework web minimalista para Python.
import web
# Importa el módulo 'sqlite3', que proporciona una interfaz SQL compatible con DB-API 2.0 para la base de datos SQLite.
import sqlite3

# Define una tupla 'urls' que mapea patrones de URL a clases que manejarán esas rutas.
# Cada par es (patrón_URL, nombre_de_clase).
urls = (
    # La ruta raíz "/" será manejada por la clase 'Index'.
    "/", "Index",
    # La ruta "/insertar" será manejada por la clase 'Insertar'.
    "/insertar", "Insertar",
    # La ruta "/detalle/(.*)" captura cualquier cosa después de "/detalle/" como un parámetro (id_persona),
    # y será manejada por la clase 'Detalle'.
    "/detalle/(.*)", "Detalle",
    # Similarmente, "/editar/(.*)" es para la clase 'Editar', capturando el ID.
    "/editar/(.*)", "Editar",
    # Y "/borrar/(.*)" es para la clase 'Borrar', capturando el ID.
    "/borrar/(.*)", "Borrar"
)

# Crea un objeto 'render' utilizando web.template.render().
# Esto configura el motor de plantillas para buscar archivos HTML en la carpeta "templates/".
# Las funciones de renderización generadas por este objeto (ej. render.index(), render.insertar())
# se usarán para mostrar las vistas HTML.
render = web.template.render("templates/")

# Crea una instancia de la aplicación web.py.
# 'urls' define el mapeo de URLs.
# 'globals()' pasa el contexto global, permitiendo a web.py encontrar las clases de manejo de rutas
# (Index, Insertar, Detalle, Editar, Borrar) definidas en este módulo.
app = web.application(urls, globals())

# Define la clase 'Index', que manejará las solicitudes HTTP a la ruta raíz ("/").
class Index:
    # Este método se ejecuta cuando se recibe una solicitud HTTP GET a la ruta asociada.
    def GET(self):
        try:
            # Intenta establecer una conexión con la base de datos SQLite llamada "agenda.db".
            conection = sqlite3.connect("agenda.db")
            # Crea un objeto cursor, que permite ejecutar comandos SQL.
            cursor = conection.cursor()
            # Ejecuta una consulta SQL para seleccionar todos los registros de la tabla 'personas'.
            personas = cursor.execute("select * from personas;")
            # Prepara un diccionario 'respuesta' para pasar a la plantilla.
            respuesta = {
                # Obtiene todas las filas resultantes de la consulta y las almacena en "personas".
                "personas" : personas.fetchall(),
                # Inicializa "error" a None, indicando que no hay errores.
                "error": None
            }
            # Renderiza la plantilla 'index.html' (ubicada en 'templates/index.html')
            # y le pasa el diccionario 'respuesta' como contexto.
            return render.index(respuesta)
        # Captura específicamente errores operacionales de SQLite (ej. base de datos no encontrada, tabla no existe).
        except sqlite3.OperationalError as error:
            # Imprime un mensaje de error en la consola para depuración.
            print(f"Error 000: {error.args[0]}")
            # Prepara una respuesta con una lista vacía de personas y un mensaje de error.
            respuesta = {
                "personas" : [],
                "error": "Error en la base de datos"
            }
            # Imprime la respuesta de error para depuración.
            print(f"RESPUESTA: {respuesta}")
            # Renderiza la plantilla 'index.html' con el mensaje de error.
            return render.index(respuesta)

# Define la clase 'Insertar', que manejará las solicitudes para la ruta "/insertar".
class Insertar:
    # Este método se ejecuta cuando se recibe una solicitud HTTP GET a la ruta "/insertar".
    def GET(self):
        try:
            # Simplemente renderiza la plantilla 'insertar.html' para mostrar el formulario de inserción.
            return render.insertar()
        # Captura cualquier otra excepción que pueda ocurrir durante la renderización.
        except Exception as error:
            # Imprime un mensaje de error genérico.
            print(f"Error 001: {error.args[0]}")
            # A pesar del error, intenta renderizar la plantilla.
            return render.insertar()

    # Este método se ejecuta cuando se recibe una solicitud HTTP POST a la ruta "/insertar"
    # (es decir, cuando se envía el formulario de inserción).
    def POST(self):
        try:
            # Obtiene los datos enviados en el formulario (campos 'nombre' y 'email').
            form = web.input()
            # Imprime los datos del formulario para depuración.
            print(f"Form data: {form}")
            # Establece una conexión con la base de datos.
            conection = sqlite3.connect("agenda.db")
            # Crea un objeto cursor.
            cursor = conection.cursor()
            # Define la consulta SQL para insertar un nuevo registro. Los '?' son marcadores de posición.
            sql = "INSERT INTO personas(nombre, email) VALUES (?, ?);"
            # Prepara los datos a insertar como una tupla, en el orden de los marcadores de posición.
            data = (form.nombre, form.email)
            # Ejecuta la consulta SQL con los datos proporcionados.
            cursor.execute(sql, data)
            # Imprime un mensaje de éxito en la consola.
            print("Executed SQL query successfully.")
            # Confirma los cambios en la base de datos (hace que la inserción sea permanente).
            conection.commit()
            # Cierra la conexión a la base de datos.
            conection.close()
            # Redirige al usuario a la página principal ("/") después de la inserción exitosa.
            return web.seeother("/")
        # Captura errores operacionales específicos de SQLite durante la inserción.
        except sqlite3.OperationalError as error:
            # Imprime el error para depuración.
            print(f"Error 002: {error.args[0]}")
            # Redirige a la página principal incluso si hay un error en la DB.
            return web.seeother("/")
        # Captura cualquier otra excepción inesperada durante el POST.
        except Exception as error:
            # Imprime el error genérico.
            print(f"Error 003: {error.args[0]}")
            # Redirige a la página principal.
            return web.seeother("/")

# Define la clase 'Detalle', que manejará las solicitudes para la ruta "/detalle/(.*)".
class Detalle:
    # Este método se ejecuta con una solicitud HTTP GET, recibiendo el ID de la persona de la URL.
    def GET(self, id_persona):
        try:
            # Establece la conexión a la base de datos.
            conection = sqlite3.connect("agenda.db")
            # Crea un cursor.
            cursor = conection.cursor()
            # Define la consulta SQL para seleccionar una persona específica por su ID.
            sql = "select * from personas where id_persona = ?;"
            # Prepara los datos para la consulta (el ID de la persona).
            datos = (id_persona,)
            # Ejecuta la consulta.
            personas = cursor.execute(sql,datos)
            # Prepara la respuesta para la plantilla.
            respuesta={
                # Obtiene la primera (y única) fila que coincide con el ID.
                "persona" : personas.fetchone(),
                "error": None
            }
            # Imprime la respuesta para depuración.
            print(f"RESPUESTA: {respuesta}")
            # Renderiza la plantilla 'detalle.html' con los datos de la persona.
            return render.detalle(respuesta)
        # Captura errores operacionales de SQLite.
        except sqlite3.OperationalError as error:
            # Imprime el error.
            print(f"Error 004: {error.args[0]}")
            # Prepara una respuesta con un diccionario vacío para 'persona' y un mensaje de error.
            respuesta={
                "persona" : {},
                "error": "Error en la base de datos"
            }
            # Renderiza la plantilla 'detalle.html' con el error.
            return render.detalle(respuesta)

# Define la clase 'Editar', que manejará las solicitudes para la ruta "/editar/(.*)".
class Editar:
    # Este método se ejecuta con una solicitud HTTP GET para mostrar el formulario de edición.
    def GET(self, id_persona):
        try:
            # Establece la conexión a la base de datos.
            conection = sqlite3.connect("agenda.db")
            # Crea un cursor.
            cursor = conection.cursor()
            # Define la consulta SQL para obtener los datos de la persona a editar.
            sql = "select * from personas where id_persona = ?;"
            # Prepara los datos para la consulta.
            datos = (id_persona,)
            # Ejecuta la consulta y obtiene la primera fila.
            persona = cursor.execute(sql, datos).fetchone()
            # Prepara la respuesta para la plantilla.
            respuesta = {
                "persona": persona,
                "error": None
            }
            # Renderiza la plantilla 'editar.html' con los datos de la persona.
            return render.editar(respuesta)
        # Captura cualquier excepción durante la obtención de datos para la edición.
        except Exception as error:
            # Imprime el error.
            print(f"Error 005: {error.args[0]}")
            # Prepara una respuesta indicando que la persona no se pudo obtener.
            respuesta = {
                "persona": None,
                "error": "Error al obtener la persona"
            }
            # Renderiza la plantilla 'editar.html' con el mensaje de error.
            return render.editar(respuesta)

    # Este método se ejecuta con una solicitud HTTP POST para procesar el formulario de edición.
    def POST(self, id_persona):
        try:
            # Obtiene los datos enviados en el formulario (nombre y email actualizados).
            form = web.input()
            # Establece la conexión a la base de datos.
            conection = sqlite3.connect("agenda.db")
            # Crea un cursor.
            cursor = conection.cursor()
            # Define la consulta SQL para actualizar los datos de la persona.
            sql = "UPDATE personas SET nombre = ?, email = ? WHERE id_persona = ?;"
            # Prepara los datos para la actualización (nombre, email, y el ID de la persona).
            data = (form.nombre, form.email, id_persona)
            # Ejecuta la consulta de actualización.
            cursor.execute(sql, data)
            # Confirma los cambios en la base de datos.
            conection.commit()
            # Cierra la conexión.
            conection.close()
            # Redirige al usuario a la página principal después de la actualización exitosa.
            return web.seeother("/")
        # Captura cualquier excepción durante la actualización.
        except Exception as error:
            # Imprime el error.
            print(f"Error 006: {error.args[0]}")
            # Redirige a la página principal incluso si hay un error.
            return web.seeother("/")

# Define la clase 'Borrar', que manejará las solicitudes para la ruta "/borrar/(.*)".
class Borrar:
    # Este método se ejecuta con una solicitud HTTP GET para eliminar un registro.
    # Nota: En un entorno de producción, las eliminaciones deberían ser POST para mayor seguridad.
    def GET(self, id_persona):
        try:
            # Establece la conexión a la base de datos.
            conection = sqlite3.connect("agenda.db")
            # Crea un cursor.
            cursor = conection.cursor()
            # Define la consulta SQL para eliminar una persona por su ID.
            sql = "DELETE FROM personas WHERE id_persona = ?;"
            # Ejecuta la consulta de eliminación.
            cursor.execute(sql, (id_persona,)) # La tupla (id_persona,) es necesaria para un solo elemento.
            # Confirma los cambios en la base de datos.
            conection.commit()
            # Cierra la conexión.
            conection.close()
            # Redirige al usuario a la página principal después de la eliminación exitosa.
            return web.seeother("/")
        # Captura cualquier excepción durante la eliminación.
        except Exception as error:
            # Imprime el error.
            print(f"Error 007: {error.args[0]}")
            # Redirige a la página principal incluso si hay un error.
            return web.seeother("/")

# Obtiene la aplicación como una función WSGI (Web Server Gateway Interface).
# Esto la hace compatible con servidores web WSGI como Gunicorn, uWSGI, etc.
application = app.wsgifunc()

# Este bloque se ejecuta solo si el script se ejecuta directamente (no cuando se importa como un módulo).
if __name__ == "__main__":
    # Inicia el servidor web de desarrollo de web.py.
    # Esto hace que la aplicación sea accesible en un navegador (típicamente en http://localhost:8080).
    app.run()