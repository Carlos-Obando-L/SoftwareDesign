"""
Módulo que implementa el patrón Factory para crear pedidos.

Se implementa el patrón Factory Method para desacoplar la creación de objetos
de su uso en el código cliente.

VENTAJAS:
1. **Extensibilidad**: Permite agregar nuevos tipos de pedidos sin modificar
   el código existente (Principio Open/Closed).
2. **Desacoplamiento**: El código cliente (main.py) no necesita conocer las
   clases concretas de pedidos, solo trabaja con la interfaz Pedido.
3. **Mantenibilidad**: Centraliza la lógica de creación, facilitando cambios
   futuros en la inicialización de objetos.
4. **Flexibilidad**: Permite tener diferentes factories para diferentes familias
   de productos (hamburguesas, pizzas, ensaladas, bebidas, etc.).

ESTRUCTURA:
- CreadorPedidos: Clase abstracta que define la interfaz factory
- CreadorHamburguesas, CreadorPizzas: Factories concretas para cada tipo de pedido

EJEMPLO DE USO:
    factory = CreadorHamburguesas()
    pedido = factory.crear_pedido(1)  # Crea un PedidoHamburguesa con id 1
"""

from abc import ABC, abstractmethod
from pedido import Pedido, PedidoHamburguesa, PedidoPizza

class CreadorPedidos(ABC):
    """
    Clase abstracta Factory para crear pedidos.
    Define la interfaz que deben implementar todas las factories concretas.
    Esta clase utiliza el patrón Factory Method, donde el método crear_pedido()
    actúa como el factory method.
    """
    
    @abstractmethod
    def crear_pedido(self, numero_pedido: int) -> Pedido:
        """
        Método factory para crear un pedido específico.
        Este es el Factory Method que debe ser implementado por cada
        factory concreta para crear su tipo específico de pedido.
        Args:
            numero_pedido: Identificador único del pedido a crear 
        Returns:
            Pedido: Una instancia de un tipo concreto de Pedido
        """
        pass

class CreadorHamburguesas(CreadorPedidos):
    """
    Factory concreta para crear pedidos de hamburguesas.
    Esta clase implementa el Factory Method para crear instancias
    específicas de PedidoHamburguesa.
    """
    
    def crear_pedido(self, numero_pedido: int) -> Pedido:
        """
        Crea un nuevo pedido de hamburguesa.
        Args:
            numero_pedido: Identificador único del pedido
        Returns:
            PedidoHamburguesa: Una nueva instancia de pedido de hamburguesa
        """
        return PedidoHamburguesa(numero_pedido)


class CreadorPizzas(CreadorPedidos):
    """
    Factory concreta para crear pedidos de pizzas.
    Esta clase implementa el Factory Method para crear instancias
    específicas de PedidoPizza.
    """
    
    def crear_pedido(self, numero_pedido: int) -> Pedido:
        """
        Crea un nuevo pedido de pizza.
        Args:
            numero_pedido: Identificador único del pedido
        Returns:
            PedidoPizza: Una nueva instancia de pedido de pizza
        """
        return PedidoPizza(numero_pedido)
