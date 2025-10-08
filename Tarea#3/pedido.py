"""
Módulo que define la clase base Pedido y sus implementaciones concretas.

Se utiliza el patrón Template Method a través de la clase abstracta Pedido.
Esto permite definir una interfaz común para todos los tipos de pedidos,
facilitando la extensión del sistema con nuevos tipos sin modificar el código
existente (Principio Open/Closed de SOLID).

La clase abstracta define dos métodos principales:
- preparar(): Retorna la descripción del pedido preparado
- get_tipo(): Retorna el tipo de pedido para logging y seguimiento

Cada tipo de pedido concreto implementa estos métodos según sus características
específicas.
"""

from abc import ABC, abstractmethod

class Pedido(ABC):
    """
    Clase abstracta que representa un pedido genérico.
    Esta clase sirve como base para todos los tipos de pedidos en el sistema.
    Define la interfaz que deben implementar todas las clases concretas de 
    pedidos.
    Attributes:
        numero_pedido (int): Identificador único del pedido
    """
    
    def __init__(self, numero_pedido: int):
        self.numero_pedido = numero_pedido
    
    @abstractmethod
    def preparar(self) -> str:
        """
        Método abstracto para preparar el pedido.
        Este método debe ser implementado por cada clase concreta para definir
        cómo se prepara el pedido específico.
        Returns:
            str: Mensaje describiendo el pedido preparado
        """
        pass
    
    @abstractmethod
    def get_tipo(self) -> str:
        """
        Retorna el tipo de pedido.
        Este método permite identificar el tipo de pedido sin necesidad de
        usar isinstance(), facilitando el logging y seguimiento.
        Returns:
            str: Tipo de pedido (ej: "Hamburguesa", "Pizza")
        """
        pass


class PedidoHamburguesa(Pedido):
    """
    Implementación concreta de un pedido de hamburguesa.
    Las hamburguesas son pedidos rápidos con un tiempo de preparación estándar.
    """
    
    def __init__(self, numero_pedido: int):
        """
        Inicializa un pedido de hamburguesa.
        Args:
            numero_pedido: Identificador único del pedido
        """
        super().__init__(numero_pedido)
    
    def preparar(self) -> str:
        """
        Prepara la hamburguesa.
        Returns:
            str: Mensaje indicando que la hamburguesa fue preparada
        """
        return f"Hamburguesa {self.numero_pedido} preparada"
    
    def get_tipo(self) -> str:
        """
        Retorna el tipo de pedido.
        Returns:
            str: "Hamburguesa"
        """
        return "Hamburguesa"


class PedidoPizza(Pedido):
    """
    Implementación concreta de un pedido de pizza.
    Las pizzas pueden tener un tiempo de preparación ligeramente mayor
    que las hamburguesas debido a su complejidad.
    """
    
    def __init__(self, numero_pedido: int):
        """
        Inicializa un pedido de pizza.
        Args:
            numero_pedido: Identificador único del pedido
        """
        super().__init__(numero_pedido)
    
    def preparar(self) -> str:
        """
        Prepara la pizza.
        Returns:
            str: Mensaje indicando que la pizza fue preparada
        """
        return f"Pizza {self.numero_pedido} preparada"
    
    def get_tipo(self) -> str:
        """
        Retorna el tipo de pedido.
        Returns:
            str: "Pizza"
        """
        return "Pizza"
