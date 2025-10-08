"""
Módulo que implementa el servicio de gestión de pedidos con concurrencia.

Se implementa una arquitectura Producer-Consumer donde:
- PRODUCER: El código cliente (main.py) produce pedidos y los agrega a la cola
- CONSUMER: Los cocineros (workers) consumen pedidos de la cola y los procesan
- QUEUE: Cola thread-safe que coordina la comunicación entre producers y consumers

VENTAJAS DE ESTA ARQUITECTURA:
1. **Desacoplamiento**: Producers y consumers no se conocen entre sí
2. **Balance de carga**: La cola distribuye trabajo automáticamente
3. **Thread-safety**: Queue de Python maneja toda la sincronización interna
4. **Escalabilidad**: Fácil ajustar el número de workers según la carga

SINCRONIZACIÓN Y THREAD-SAFETY:
Se utilizan tres mecanismos de sincronización:

1. **Queue (Cola thread-safe)**:
   - Implementada en queue.Queue de Python
   - Usa locks internos para operaciones atómicas (put, get)
   - Método join() espera hasta que todos los items sean procesados
   - Método task_done() notifica que un item ha sido procesado
2. **Lock (threading.Lock)**:
   - Sincroniza acceso a recursos compartidos (salida a consola)
   - Previene race conditions en operaciones de I/O
   - Asegura que los mensajes no se mezclen entre threads
3. **Thread.join()**:
   - Espera a que los threads terminen antes de continuar
   - Asegura cleanup ordenado de recursos

FLUJO DE EJECUCIÓN:
1. Cliente agrega pedidos a la cola (agregar_pedido)
2. procesar_pedidos() crea y arranca los cocineros
3. Cocineros consumen pedidos concurrentemente
4. join() espera a que la cola esté vacía
5. "Poison pills" (None) detienen a los cocineros
6. join() en threads espera a que terminen limpiamente
"""

import threading
from queue import Queue
from typing import List
from pedido import Pedido
from cocinero import Cocinero


class ServicioPedidos:
    """
    Clase que gestiona el procesamiento de pedidos usando múltiples cocineros (hilos).
    Implementa el patrón Producer-Consumer con un Thread Pool de cocineros.
    La clase actúa como coordinador entre los producers (código cliente) y
    consumers (cocineros).
    RESPONSABILIDADES:
    - Mantener una cola thread-safe de pedidos
    - Gestionar el ciclo de vida del pool de cocineros
    - Coordinar la sincronización entre threads
    - Proporcionar interfaz simple para agregar y procesar pedidos
    Attributes:
        cola_pedidos (Queue): Cola thread-safe para almacenar pedidos pendientes
        num_cocineros (int): Número de cocineros (workers) en el pool
        cocineros (List[Cocinero]): Lista de cocineros activos
        lock (threading.Lock): Lock compartido para sincronización de I/O
        pedidos_totales (int): Contador total de pedidos agregados
    """
    
    def __init__(self, num_cocineros: int = 2):
        """
        Inicializa el servicio de pedidos.
        Args:
            num_cocineros: Número de cocineros (hilos) que procesarán los 
            pedidos. Default: 2 cocineros para balance entre concurrencia y
            recursos.
        """
        # Queue: Cola FIFO thread-safe de Python
        # Características:
        # - put() y get() son operaciones atómicas
        # - Bloqueo automático cuando está vacía (get) o llena (put con maxsize)
        # - Tracking interno de tareas pendientes para join()
        self.cola_pedidos = Queue()
        
        self.num_cocineros = num_cocineros
        self.cocineros: List[Cocinero] = []
        
        # Lock compartido para sincronizar salidas a consola
        # Previene que múltiples threads escriban simultáneamente
        self.lock = threading.Lock()
    
    def agregar_pedido(self, pedido: Pedido):
        """
        Agrega un pedido a la cola para ser procesado (operación Producer).
        Esta operación es thread-safe gracias a Queue.put(), que usa locks
        internos para garantizar atomicidad.
        Args:
            pedido: El pedido a agregar a la cola
        THREAD-SAFETY: Queue.put() es thread-safe, múltiples threads pueden
        agregar pedidos concurrentemente sin problemas.
        """
        self.cola_pedidos.put(pedido)
    
    def procesar_pedidos(self):
        """
        Inicia el procesamiento de todos los pedidos en la cola.
        FLUJO DE EJECUCIÓN:
        1. Crear pool de cocineros (workers)
        2. Iniciar todos los cocineros (threads)
        3. Esperar a que procesen todos los pedidos (join en cola)
        4. Enviar señales de parada (poison pills)
        5. Esperar a que los threads terminen (join en threads)
        6. Cleanup y logging final
        SINCRONIZACIÓN CRÍTICA:
        - cola_pedidos.join(): Bloquea hasta que todos los pedidos sean procesados
        - cocinero.join(): Bloquea hasta que cada thread termine limpiamente
        """
        # FASE 1: Crear e iniciar el pool de cocineros
        # Cada cocinero es un thread que consumirá de la cola compartida
        for i in range(self.num_cocineros):
            cocinero = Cocinero(
                nombre=f"COCINERO {i + 1}",
                cola_pedidos=self.cola_pedidos,
                lock=self.lock
            )
            self.cocineros.append(cocinero)
            # start() inicia el thread (ejecuta el método run() en paralelo)
            cocinero.start()
        
        # FASE 2: Esperar a que se procesen todos los pedidos
        # join() bloquea hasta que:
        # - La cola esté vacía, Y
        # - Todos los task_done() hayan sido llamados
        # Esto asegura que todos los pedidos han sido completamente procesados
        self.cola_pedidos.join()
        
        # FASE 3: Enviar señales de parada a todos los cocineros
        # "Poison pill" pattern: None indica al worker que debe terminar
        # Enviamos uno por cada cocinero para que todos reciban la señal
        for _ in range(self.num_cocineros):
            self.cola_pedidos.put(None)
        
        # FASE 4: Esperar a que todos los cocineros terminen limpiamente
        # join() en cada thread bloquea hasta que el thread termine
        # Esto asegura cleanup ordenado y previene zombie threads
        for cocinero in self.cocineros:
            cocinero.join()
        
        # FASE 5: Logging final y cleanup
        with self.lock:
            print("[SISTEMA] Todos los pedidos procesados")
        
        # Limpiar la lista de cocineros para futuras ejecuciones
        self.cocineros.clear()
