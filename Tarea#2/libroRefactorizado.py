class Libro:
    """Representa un libro en la biblioteca."""
    def __init__(self, titulo, autor, genero, paginas, anio_publicacion, disponible=True):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._paginas = paginas
        self._anio_publicacion = anio_publicacion
        self._disponible = disponible

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    @property
    def paginas(self):
        return self._paginas

    @property
    def anio_publicacion(self):
        return self._anio_publicacion

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = valor

    def calcular_popularidad(self):
        if self._genero == 'novela':
            base = 50
            extra = self._paginas / 10
        elif self._genero == 'ciencia':
            base = 70
            extra = self._paginas / 5
        elif self._genero == 'historia':
            base = 40
            extra = self._paginas / 8
        else:
            base = 10
            extra = 0
        return base + extra

    def es_antiguo(self):
        return self._anio_publicacion < 1980

    def obtener_info(self):
        return {
            "Título": self._titulo,
            "Autor": self._autor,
            "Género": self._genero,
            "Páginas": self._paginas,
            "Año": self._anio_publicacion,
            "Disponible": "Sí" if self._disponible else "No",
            "Popularidad": self.calcular_popularidad(),
            "Es antiguo": "Sí" if self.es_antiguo() else "No"
        }

    def imprimir_info(self):
        info = self.obtener_info()
        for clave, valor in info.items():
            print(f"{clave}: {valor}")
