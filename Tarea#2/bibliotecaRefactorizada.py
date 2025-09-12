from libroRefactorizado import Libro

class Biblioteca:
    """Gestiona una colección de libros."""
    def __init__(self):
        self._libros = []

    def agregar_libro(self, libro):
        if isinstance(libro, Libro):
            self._libros.append(libro)
        else:
            raise ValueError("Solo se pueden agregar instancias de Libro.")

    def buscar_libro(self, titulo):
        return [libro for libro in self._libros if libro.titulo.lower() == titulo.lower()]

    def eliminar_libro(self, titulo):
        self._libros = [libro for libro in self._libros if libro.titulo.lower() != titulo.lower()]

    def listar_libros(self):
        return [libro.obtener_info() for libro in self._libros]

    def generar_reporte(self):
        total = len(self._libros)
        antiguos = sum(1 for l in self._libros if l.es_antiguo())
        disponibles = sum(1 for l in self._libros if l.disponible)
        popularidad_total = sum(l.calcular_popularidad() for l in self._libros)
        promedio_popularidad = popularidad_total / total if total > 0 else 0
        return {
            "Total libros": total,
            "Disponibles": disponibles,
            "Antiguos": antiguos,
            "Promedio de popularidad": promedio_popularidad
        }
