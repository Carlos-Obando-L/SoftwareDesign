"""
Módulo que implementa la clase Cocinero como un worker thread.

Se implementa el patrón Worker Thread (también conocido como Thread Pool Worker)
donde cada cocinero es un hilo que consume tareas de una cola compartida.

VENTAJAS DE ESTA ARQUITECTURA:
1. **Concurrencia real**: Múltiples cocineros procesan pedidos simultáneamente
2. **Distribución de carga**: Los pedidos se distribuyen automáticamente entre
   los cocineros disponibles
3. **Escalabilidad**: Fácil agregar o quitar cocineros sin cambiar la lógica
4. **Eficiencia**: Los hilos reutilizan recursos en lugar de crear nuevos hilos
   por cada pedido

SINCRONIZACIÓN:
- Queue: Cola thread-safe de Python (usa locks internamente)
- Lock: Para sincronizar salidas a consola y evitar texto entremezclado
- task_done(): Notifica cuando un pedido ha sido procesado completamente

MANEJO DE PARADA:
- Señal None: Usado como "poison pill" para detener threads de forma limpia
- daemon=True: Asegura que los threads no bloqueen el cierre del programa
- timeout en get(): Permite verificar periódicamente si debe detenerse
"""

import threading
import time
from queue import Empty, Queue
from pedido import Pedido


class Cocinero(threading.Thread):
    """
    Clase que representa un cocinero como un hilo de trabajo (worker thread).
    Cada cocinero es un hilo independiente que:
    1. Consume pedidos de una cola compartida thread-safe
    2. Procesa cada pedido (simula preparación)
    3. Registra el progreso de forma sincronizada
    La clase hereda de threading.Thread para implementar el comportamiento
    de un worker en un pool de threads.
    Attributes:
        nombre (str): Identificador del cocinero para logging
        cola_pedidos (Queue): Cola compartida thread-safe de pedidos
        lock (threading.Lock): Lock para sincronizar salidas a consola
        activo (bool): Flag para controlar el ciclo de vida del thread
        pedidos_procesados (int): Contador de pedidos completados
    """
    
    def __init__(self, nombre: str, cola_pedidos: Queue, lock: threading.Lock):
        """
        Inicializa un cocinero (worker thread).
        Args:
            nombre: Identificador del cocinero (ej: "COCINERO 1")
            cola_pedidos: Cola thread-safe compartida de donde se obtienen los pedidos
            lock: Lock para sincronizar la salida en consola y evitar race conditions
        """
        super().__init__()
        self.nombre = nombre
        self.cola_pedidos = cola_pedidos
        self.lock = lock
        self.activo = True
        self.pedidos_procesados = 0
        # daemon=True: El hilo se cerrará automáticamente cuando el programa
        # principal termine, evitando que threads huérfanos bloqueen el cierre
        self.daemon = True
    
    def run(self):
        """
        Método principal del hilo que procesa pedidos continuamente.
        Este método se ejecuta en un hilo separado cuando se llama a start().
        Implementa el patrón Consumer, consumiendo pedidos de la cola hasta
        recibir una señal de parada (None).
        SINCRONIZACIÓN:
        - get(timeout=1): Timeout para evitar bloqueo indefinido y permitir
          verificaciones periódicas del estado
        - task_done(): Notifica a la cola que el pedido ha sido procesado,
          necesario para join() en ServicioPedidos
        """
        while self.activo:
            try:
                # Intentar obtener un pedido con timeout de 1 segundo
                # Esto evita bloqueo indefinido y permite verificar self.activo
                pedido = self.cola_pedidos.get(timeout=1)
                
                # None es la "poison pill" - señal para terminar el hilo
                if pedido is None:
                    self.cola_pedidos.task_done()
                    break
                
                # Procesar el pedido
                self._procesar_pedido(pedido)
                
                # Notificar a la cola que el pedido ha sido procesado
                # Esto es crucial para queue.join() en ServicioPedidos
                self.cola_pedidos.task_done()
                
            except Empty:
                # Timeout alcanzado sin obtener pedido - la cola está vacía
                # Continuar esperando por más pedidos
                continue
            except Exception as e:
                # Manejo de errores inesperados
                with self.lock:
                    print(f"[{self.nombre}] Error procesando pedido: {e}")
                continue
    
    def _procesar_pedido(self, pedido: Pedido):
        """
        Procesa un pedido individual de forma sincronizada.
        Este método simula la preparación de un pedido con las siguientes etapas:
        1. Cambiar estado del pedido a "en_preparacion"
        2. Log de inicio de preparación (sincronizado)
        3. Simular tiempo de preparación (sleep)
        4. Preparar el pedido (llamar al método del pedido)
        5. Cambiar estado a "completado"
        6. Log de finalización (sincronizado)
        Args:
            pedido: El pedido a procesar
        DECISIÓN: Usar lock para las salidas a consola previene que múltiples
        threads escriban simultáneamente, lo que causaría texto entremezclado
        e ilegible. El lock asegura salidas atómicas.
        """        
        # SECCIÓN CRÍTICA: Imprimir inicio de preparación
        # El lock asegura que solo un thread escriba a la vez
        with self.lock:
            print(f"[{self.nombre}] Preparando pedido {pedido.numero_pedido} ({pedido.get_tipo()})")
        
        # Preparar el pedido (obtener resultado)
        resultado = pedido.preparar()
        
        # SECCIÓN CRÍTICA: Imprimir resultado
        with self.lock:
            print(f"[{self.nombre}] Pedido {pedido.numero_pedido} listo: {resultado}")
    
    def detener(self):
        """
        Marca el cocinero para que deje de procesar pedidos.
        Este método cambia el flag 'activo' a False, lo que causará que
        el hilo termine su ejecución en la próxima iteración del loop.
        """
        self.activo = False
