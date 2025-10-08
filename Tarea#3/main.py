"""
Sistema de gestión de pedidos con concurrencia.

PATRONES DE DISEÑO IMPLEMENTADOS:

1. FACTORY METHOD (factory.py):
   - Desacopla la creación de objetos de su uso
   - Facilita agregar nuevos tipos de pedidos sin modificar código existente
2. PRODUCER-CONSUMER (servicio_pedidos.py):
   - Main actúa como Producer agregando pedidos
   - Cocineros actúan como Consumers procesando pedidos
3. WORKER THREAD POOL (cocinero.py):
   - Pool de threads que procesan tareas concurrentemente
   - Distribución automática de carga entre workers
4. TEMPLATE METHOD (pedido.py):
   - Clase base abstracta define interfaz común
   - Subclases implementan comportamiento específico

FLUJO DE DATOS:
1. Cliente crea pedidos usando Factories
2. Pedidos se agregan a la cola thread-safe
3. Cocineros consumen pedidos concurrentemente
4. Cada cocinero procesa pedidos de forma independiente
5. Sistema espera a que todos los pedidos se completen
"""

from servicio_pedidos import ServicioPedidos
from factory import CreadorHamburguesas, CreadorPizzas


# Main para prueba
if __name__ == "__main__":
    servicio = ServicioPedidos()

    # Factory para hamburguesas
    creador_hamburguesas = CreadorHamburguesas()
    for i in range(3):
        pedido = creador_hamburguesas.crear_pedido(i)
        servicio.agregar_pedido(pedido)
    
    # Factory para pizzas
    creador_pizzas = CreadorPizzas()
    for i in range(3):
        pedido = creador_pizzas.crear_pedido(i)
        servicio.agregar_pedido(pedido)

    servicio.procesar_pedidos()