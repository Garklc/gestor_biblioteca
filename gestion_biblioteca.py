# gestor_biblioteca.py

class Libro:
    def __init__(self, titulo, autor, ano_publicacion, estado="Disponible"):
        self.__titulo = titulo
        self.__autor = autor
        self.__ano_publicacion = ano_publicacion
        self.__estado = estado

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_ano_publicacion(self):
        return self.__ano_publicacion

    def get_estado(self):
        return self.__estado

    def set_titulo(self, nuevo_titulo):
        self.__titulo = nuevo_titulo

    def set_autor(self, nuevo_autor):
        self.__autor = nuevo_autor

    def set_ano_publicacion(self, nuevo_ano):
        self.__ano_publicacion = nuevo_ano

    def set_estado(self, nuevo_estado):
        self.__estado = nuevo_estado

    def __str__(self):
        return f"Título: {self.__titulo}, Autor: {self.__autor}, Año: {self.__ano_publicacion}, Estado: {self.__estado}"


class LibroDigital(Libro):
    def __init__(self, titulo, autor, ano_publicacion, formato, estado="Disponible"):
        super().__init__(titulo, autor, ano_publicacion, estado)
        self.__formato = formato

    def get_formato(self):
        return self.__formato

    def set_formato(self, nuevo_formato):
        self.__formato = nuevo_formato

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Formato: {self.__formato}"


import json

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.cargar_libros()

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def eliminar_libro(self, titulo):
        for libro in self.libros:
            if libro.get_titulo() == titulo:
                self.libros.remove(libro)
                print(f"Libro '{titulo}' eliminado exitosamente.")
                return
        print(f"No se encontró ningún libro con el título '{titulo}'.")

    def listar_libros_disponibles(self):
        disponibles = [libro for libro in self.libros if libro.get_estado() == "Disponible"]
        if disponibles:
            print("Libros Disponibles:")
            for libro in disponibles:
                print(libro)
        else:
            print("No hay libros disponibles en este momento.")

    def buscar_libro_por_titulo(self, titulo):
        for libro in self.libros:
            if libro.get_titulo() == titulo:
                print(f"Libro encontrado:\n{libro}")
                return
        print(f"No se encontró ningún libro con el título '{titulo}'.")

    def marcar_como_prestado(self, titulo):
        for libro in self.libros:
            if libro.get_titulo() == titulo:
                if libro.get_estado() == "Disponible":
                    libro.set_estado("Prestado")
                    print(f"El libro '{titulo}' ha sido marcado como Prestado.")
                else:
                    print(f"El libro '{titulo}' ya está Prestado.")
                return
        print(f"No se encontró ningún libro con el título '{titulo}'.")

    def devolver_libro(self, titulo):
        for libro in self.libros:
            if libro.get_titulo() == titulo:
                if libro.get_estado() == "Prestado":
                    libro.set_estado("Disponible")
                    print(f"El libro '{titulo}' ha sido devuelto y ahora está Disponible.")
                else:
                    print(f"El libro '{titulo}' no estaba Prestado.")
                return
        print(f"No se encontró ningún libro con el título '{titulo}'.")

    def cargar_libros(self):
        try:
            with open("biblioteca.txt", "r") as file:
                data = json.load(file)
                for libro_data in data:
                    if libro_data["tipo"] == "Libro":
                        libro = Libro(
                            libro_data["titulo"],
                            libro_data["autor"],
                            libro_data["ano_publicacion"],
                            libro_data["estado"]
                        )
                    elif libro_data["tipo"] == "LibroDigital":
                        libro = LibroDigital(
                            libro_data["titulo"],
                            libro_data["autor"],
                            libro_data["ano_publicacion"],
                            libro_data["formato"],
                            libro_data["estado"]
                        )
                    self.libros.append(libro)
        except FileNotFoundError:
            print("El archivo biblioteca.txt no existe. Se creará uno nuevo al guardar cambios.")

    def guardar_libros(self):
        data = []
        for libro in self.libros:
            libro_data = {
                "tipo": "LibroDigital" if isinstance(libro, LibroDigital) else "Libro",
                "titulo": libro.get_titulo(),
                "autor": libro.get_autor(),
                "ano_publicacion": libro.get_ano_publicacion(),
                "estado": libro.get_estado()
            }
            if isinstance(libro, LibroDigital):
                libro_data["formato"] = libro.get_formato()
            data.append(libro_data)

        with open("biblioteca.txt", "w") as file:
            json.dump(data, file, indent=4)
        print("Cambios guardados en el archivo biblioteca.txt.")


# --- MENÚ PRINCIPAL ---
def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Gestor de Biblioteca ---")
        print("1. Agregar libro")
        print("2. Eliminar libro")
        print("3. Ver todos los libros")
        print("4. Buscar libro")
        print("5. Marcar libro como prestado")
        print("6. Devolver libro")
        print("7. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            tipo = input("¿Es un libro físico (F) o digital (D)? ").upper()
            if tipo == "F":
                titulo = input("Título: ")
                autor = input("Autor: ")
                ano = int(input("Año de Publicación: "))
                libro = Libro(titulo, autor, ano)
                biblioteca.agregar_libro(libro)
            elif tipo == "D":
                titulo = input("Título: ")
                autor = input("Autor: ")
                ano = int(input("Año de Publicación: "))
                formato = input("Formato (PDF, ePub): ")
                libro = LibroDigital(titulo, autor, ano, formato)
                biblioteca.agregar_libro(libro)
            else:
                print("Opción inválida.")

        elif opcion == "2":
            titulo = input("Título del libro a eliminar: ")
            biblioteca.eliminar_libro(titulo)

        elif opcion == "3":
            biblioteca.listar_libros_disponibles()

        elif opcion == "4":
            titulo = input("Título del libro a buscar: ")
            biblioteca.buscar_libro_por_titulo(titulo)

        elif opcion == "5":
            titulo = input("Título del libro a marcar como prestado: ")
            biblioteca.marcar_como_prestado(titulo)

        elif opcion == "6":
            titulo = input("Título del libro a devolver: ")
            biblioteca.devolver_libro(titulo)

        elif opcion == "7":
            biblioteca.guardar_libros()
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, elige una opción válida.")

# Ejecutar el programa
if __name__ == "__main__":
    menu()