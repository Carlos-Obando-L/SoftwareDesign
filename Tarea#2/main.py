from bibliotecaRefactorizada import Biblioteca
from libroRefactorizado import Libro

def solicitar_datos_libro():
    while True:
        try:
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Género (novela/ciencia/historia): ").lower()
            paginas = int(input("Número de páginas: "))
            anio = int(input("Año de publicación: "))
            return Libro(titulo, autor, genero, paginas, anio)
        except ValueError:
            print("Por favor, ingrese datos válidos.")

if __name__ == "__main__":
    biblioteca = Biblioteca()
    while True:
        print("\n1. Agregar libro\n2. Listar libros\n3. Buscar libro\n4. Eliminar libro\n5. Generar reporte\n6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            libro = solicitar_datos_libro()
            biblioteca.agregar_libro(libro)
        elif opcion == "2":
            for info in biblioteca.listar_libros():
                print(info)
        elif opcion == "3":
            titulo = input("Título a buscar: ")
            resultados = biblioteca.buscar_libro(titulo)
            for libro in resultados:
                print(libro.obtener_info())
        elif opcion == "4":
            titulo = input("Título a eliminar: ")
            biblioteca.eliminar_libro(titulo)
            print("Libro(s) eliminado(s).")
        elif opcion == "5":
            print(biblioteca.generar_reporte())
        elif opcion == "6":
            break
        else:
            print("Opción no válida.")
