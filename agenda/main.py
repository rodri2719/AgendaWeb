import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar","Insertar",
    "/detalle/(.*)", "Detalle"
    )

render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            personas = cursor.execute("select * from personas;")
            respuesta = {
                "personas" : personas.fetchall(),
                "error": None
            }
            return render.index(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 000: {error.args[0]}")
            respuesta = {
                "personas" : [],
                "error": "Error en la base de datos"
            }
            print(f"RESPUESTA: {respuesta}")
            return render.index(respuesta)

class Insertar:
    def GET(self):
        try:
            return render.insertar()
        except Exception as error:
            print(f"Error 001: {error.args[0]}")
            return render.insertar()

    def POST(self):
        try:
            form = web.input()
            print(f"Form data: {form}")
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "INSERT INTO personas(nombre, email) VALUES (?, ?);"
            data = (form.nombre, form.email)
            cursor.execute(sql, data)
            print("Executed SQL query successfully.")
            conection.commit()
            conection.close()
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 002: {error.args[0]}")
            return web.seeother("/")
        except Exception as error:
            print(f"Error 003: {error.args[0]}")
            return web.seeother("/")


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

application = app.wsgifunc()


if __name__ == "__main__":
    app.run()