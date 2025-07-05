import web
import sqlite3
import re

urls = (
    "/", "Index",
    "/insertar","Insertar",
    "/detalle/(.*)", "Detalle",
    "/borrar/(.*)", "Borrar",
    "/editar/(.*)", "Editar"
    )

render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        mensaje = web.cookies().get("mensaje", None)
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            try:
                personas = cursor.execute("select * from personas;")
                lista = personas.fetchall()
                error = None
                if not lista:
                    error = "La base de datos está vacía."
                respuesta = {
                    "personas" : lista,
                    "error": error,
                    "mensaje": mensaje
                }
            except sqlite3.OperationalError as error:
                print(f"Error 000b: {error.args[0]}")
                respuesta = {
                    "personas" : [],
                    "error": "Error al conectar con la tabla Personas o error de sintaxis en la consulta.",
                    "mensaje": mensaje
                }
            # Limpiar cookie después de mostrar
            web.setcookie("mensaje", "", expires=-1)
            return render.index(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 000: {error.args[0]}")
            respuesta = {
                "personas" : [],
                "error": "Error al conectar con la base de datos.",
                "mensaje": mensaje
            }
            print(f"RESPUESTA: {respuesta}")
            web.setcookie("mensaje", "", expires=-1)
            return render.index(respuesta)

class Insertar:
    def GET(self):
        return render.insertar(mensaje="")

    def POST(self):
        try:
            form = web.input()
            nombre = form.nombre.strip()
            email = form.email.strip()

            # Validación de campos vacíos
            if not nombre or not email:
                return render.insertar(mensaje="Error: No se permiten campos vacíos.")

            # Validación de formato de email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return render.insertar(mensaje="Error: Formato de email inválido.")

            # Conectar con la base de datos
            try:
                conection = sqlite3.connect("agenda.db")
            except Exception as e:
                return render.insertar(mensaje="Error 3.1: No se pudo conectar a la base de datos.")

            cursor = conection.cursor()

            # Verificar si la tabla existe
            try:
                cursor.execute("SELECT COUNT(*) FROM personas;")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e).lower():
                    return render.insertar(mensaje="Error 3.2: La tabla 'personas' no existe.")
                else:
                    return render.insertar(mensaje=f"Error 3.3: {str(e)}")

            # Insertar datos
            try:
                sql = "INSERT INTO personas(nombre, email) VALUES (?, ?);"
                cursor.execute(sql, (nombre, email))
            except sqlite3.OperationalError as e:
                return render.insertar(mensaje=f"Error 3.3: Error de sintaxis en la consulta SQL.")
            except Exception as e:
                return render.insertar(mensaje=f"Error inesperado: {str(e)}")

            conection.commit()

            # Verificar si se insertó correctamente
            cursor.execute("SELECT COUNT(*) FROM personas;")
            count = cursor.fetchone()[0]
            if count == 0:
                return render.insertar(mensaje="Error 3.4: La base de datos está vacía.")

            conection.close()
            return web.seeother("/")

        except Exception as error:
            return render.insertar(mensaje=f"Error general: {error}")
        
class Detalle:

    def GET(self,id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            personas = cursor.execute(sql,datos)
            
            respuesta={
                "persona" : personas.fetchone(),
                "error": None
            }
            print(f"RESPUESTA: {respuesta}")
            return render.detalle(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 004: {error.args[0]}")
            respuesta={
                "persona" : {},
                "error": "Error en la base de datos"
            }
            return render.detalle(respuesta)

class Borrar:
    def GET(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            persona = cursor.execute(sql, datos).fetchone()
            respuesta = {
                "persona": persona,
                "error": None
            }
            return render.borrar(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 005: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos."
            }
            return render.borrar(respuesta)

    def POST(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "delete from personas where id_persona = ?;"
            datos = (id_persona,)
            cursor.execute(sql, datos)
            conection.commit()
            conection.close()
            web.setcookie("mensaje", "Dato borrado correctamente", path="/")
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 006: {error.args[0]}")
            web.setcookie("mensaje", "Error al borrar el dato", path="/")
            return web.seeother("/")

class Editar:
    def GET(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            persona = cursor.execute(sql, datos).fetchone()
            respuesta = {
                "persona": persona,
                "error": None
            }
            return render.editar(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 007: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos."
            }
            return render.editar(respuesta)

    def POST(self, id_persona):
        try:
            form = web.input()
            nombre = form.get("nombre", "").strip()
            email = form.get("email", "").strip()
            error = None
            if not nombre or not email:
                error = "No se permiten campos vacíos."
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                error = "Formato de email incorrecto."
            if error:
                persona = (id_persona, nombre, email)
                return render.editar({"persona": persona, "error": error})
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            try:
                sql = "update personas set nombre = ?, email = ? where id_persona = ?;"
                datos = (nombre, email, id_persona)
                cursor.execute(sql, datos)
                conection.commit()
                conection.close()
                return web.seeother("/")
            except sqlite3.OperationalError as error:
                print(f"Error 008b: {error.args[0]}")
                persona = (id_persona, nombre, email)
                return render.editar({"persona": persona, "error": "Error al conectar con la tabla Personas o error de sintaxis en la consulta."})
        except sqlite3.OperationalError as error:
            print(f"Error 008: {error.args[0]}")
            return render.editar({"persona": None, "error": "Error al conectar con la base de datos."})
        except Exception as error:
            print(f"Error 009: {error.args[0]}")
            return render.editar({"persona": None, "error": "Error inesperado."})

application = app.wsgifunc()


if __name__ == "__main__":
    app.run()