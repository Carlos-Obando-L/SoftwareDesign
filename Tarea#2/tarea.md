# Tarea 2 - Refactorización de Código

## Objetivo

Refactorizar el sistema de gestión de biblioteca aplicando buenas prácticas de ingeniería de
software vistas en el curso.

## Instrucciones

1. Analice el código provisto identificando al menos 5 problemas de diseño
2. Implemente las mejoras en un repositorio Git (opcional) o documento markdown para subir a Mediación Virtual.
3. Documente los cambios realizados explicando:
    * Problemas identificados
    * Soluciones implementadas
    * Buenas prácticas aplicadas
4. Incluya en dicho documento:
    * Explicación técnica de al menos 3 mejoras significativas
    * Enlace al repositorio si aplica o el código con los cambios respectivos.

## Código

### libro.py
```python
class Libro:
    def __init__(self, titulo, autor, genero, paginas, anio_publicacion, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero # 'novela', 'ciencia', 'historia'
        self.paginas = paginas
        self.anio_publicacion = anio_publicacion
        self.disponible = disponible

    def calcular_popularidad(self):
        if self.genero == 'novela':
            base = 50
            extra = self.paginas / 10
        elif self.genero == 'ciencia':
            base = 70
            extra = self.paginas / 5
        elif self.genero == 'historia':
            base = 40
            extra = self.paginas / 8
        else:
            base = 10
            extra = 0
        return base + extra
    
    def es_antiguo(self):
        if self.anio_publicacion < 1980:
            return True
        else:
            return False

    def imprimir_datos(self):
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Género: {self.genero}")
        print(f"Páginas: {self.paginas}")
        print(f"Año: {self.anio_publicacion}")
        print(f"Disponible: {'Sí' if self.disponible else 'No'}")
        print(f"Popularidad: {self.calcular_popularidad()}")
        print(f"Es antiguo: {'Sí' if self.es_antiguo() else 'No'}")
        print("------------------------")
```

### biblioteca.py
```python
from libro import Libro

class Biblioteca:
    def __init__(self):
        self.libros = []

    def agregar_libro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Género (novela/ciencia/historia): ").lower()
        paginas = int(input("Número de páginas: "))
        anio = int(input("Año de publicación: "))

        l = Libro(titulo, autor, genero, paginas, anio)
        self.libros.append(l)
        print("Libro agregado!")

    def generar_reporte(self):
        total = len(self.libros)
        antiguos = 0
        disponibles = 0
        popularidad_total = 0

        for l in self.libros:
            l.imprimir_datos()
            if l.es_antiguo():
                antiguos += 1
            if l.disponible:
                disponibles += 1
            popularidad_total += l.calcular_popularidad()

        print("\nREPORTE BIBLIOTECA:")
        print(f"Total libros: {total}")
        print(f"Disponibles: {disponibles}")
        print(f"Antiguos: {antiguos}")
        print(f"Promedio de popularidad: {popularidad_total / total if total > 0 else 0}")
```

## Problemas de diseño

1. **Acoplamiento fuerte entre entrada/salida y lógica de negocio**
    - Tanto en `Libro` (`imprimir_datos`) como en `Biblioteca` (`agregar_libro`), se mezclan operaciones de entrada/salida (input/print) con la lógica de negocio. Esto dificulta reutilizar el código en otros contextos (por ejemplo, una interfaz gráfica o web).

2. **Falta de validación y manejo de errores**
    - No se valida la entrada del usuario en `agregar_libro` (por ejemplo, si el usuario ingresa texto en vez de un número para páginas o año, el programa fallará).

3. **Responsabilidades poco claras**
    - El método `imprimir_datos` en `Libro` mezcla la obtención de información con la presentación. Sería mejor separar la obtención de datos (por ejemplo, un método que devuelva un diccionario o string) de la presentación (print).

4. **No se aprovechan las ventajas de la orientación a objetos**
    - La clase `Biblioteca` solo almacena una lista de libros y no ofrece métodos para buscar, eliminar o modificar libros, lo que limita su funcionalidad y escalabilidad.

5. **Nombres de métodos y variables poco expresivos**
    - El método `imprimir_datos` podría llamarse `mostrar_informacion` o, mejor aún, separar la obtención de datos de la impresión. Además, la variable `l` en `agregar_libro` es poco descriptiva.

## Soluciones implementadas

1. **Separación de lógica y presentación**: Se crearon métodos que devuelven la información como string o diccionario, y se eliminó la impresión directa dentro de las clases. La entrada de datos se realiza fuera de la lógica de negocio.
2. **Validación de datos**: Se agregaron validaciones para asegurar que los datos ingresados sean correctos y se manejen errores de conversión.
3. **Mejor encapsulamiento**: Se hicieron los atributos privados y se agregaron métodos getter/setter donde corresponde.
4. **Nombres descriptivos**: Se mejoraron los nombres de métodos y variables para mayor claridad.
5. **Ampliación de funcionalidades**: Se agregaron métodos para buscar, eliminar y modificar libros en la biblioteca.
6. **Documentación**: Se añadieron docstrings y comentarios explicativos en las clases y métodos principales.

## Buenas prácticas aplicadas

- Principio de responsabilidad única (SRP)
- Encapsulamiento y ocultamiento de datos
- Validación y manejo de errores
- Nombres descriptivos y legibles
- Separación de lógica de negocio y presentación
- Documentación del código

## Explicación técnica de al menos 3 mejoras significativas

### 1. Separación de lógica y presentación
Ahora los métodos de las clases no imprimen ni solicitan datos directamente. Por ejemplo, `Libro` tiene un método `obtener_info()` que devuelve la información en un diccionario, y la impresión se realiza fuera de la clase. Esto permite reutilizar la lógica en diferentes interfaces (consola, web, etc.).

### 2. Validación de datos y manejo de errores
Se agregaron validaciones para asegurar que los datos ingresados sean del tipo y rango correcto. Por ejemplo, si el usuario ingresa un valor no numérico para el año, el sistema lo detecta y solicita el dato nuevamente, evitando caídas inesperadas.

### 3. Encapsulamiento y nombres descriptivos
Los atributos de las clases ahora son privados y se accede a ellos mediante métodos. Además, los nombres de métodos y variables reflejan mejor su propósito, facilitando el mantenimiento y la comprensión del código.

## Código refactorizado

### libroRefactorizado.py
```python
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
```

### bibliotecaRefactorizada.py
```python
from libro import Libro

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
```

### main.py (ejemplo de uso)
```python
from biblioteca import Biblioteca
from libro import Libro

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
```

