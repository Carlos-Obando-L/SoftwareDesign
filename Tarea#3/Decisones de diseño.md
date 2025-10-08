# Sistema de Gestión de Pedidos con Concurrencia

## Decisiones de Diseño

### 1. Patrones Implementados

#### **Factory Method** (`factory.py`)
- **Decisión**: Desacoplar la creación de pedidos del código cliente
- **Ventaja**: Agregar nuevos tipos de pedidos sin modificar código existente (Open/Closed)
- **Estructura**: 
  - `CreadorPedidos`: Interfaz abstracta
  - `CreadorHamburguesas`, `CreadorPizzas`: Factories concretas

#### **Producer-Consumer** (`servicio_pedidos.py`)
- **Decisión**: Separar la producción de pedidos de su procesamiento
- **Ventaja**: Desacoplamiento total entre quien crea pedidos y quien los procesa
- **Implementación**: 
  - Main actúa como Producer
  - Cocineros actúan como Consumers
  - Queue coordina la comunicación

#### **Worker Thread Pool** (`cocinero.py`)
- **Decisión**: Pool de hilos que procesan tareas concurrentemente
- **Ventaja**: Distribución automática de carga, escalabilidad
- **Configuración**: 2 cocineros por defecto (balance entre concurrencia y recursos)

#### **Template Method** (`pedido.py`)
- **Decisión**: Clase abstracta define interfaz común
- **Ventaja**: Polimorfismo, fácil extensión con nuevos tipos de pedidos
- **Métodos**: `preparar()`, `get_tipo()`

---

### 2. Concurrencia y Sincronización

#### **Queue (Cola Thread-Safe)**
- **Por qué**: Cola FIFO de Python con locks internos
- **Ventajas**: 
  - Operaciones atómicas (`put()`, `get()`)
  - Sincronización automática
  - Método `join()` para esperar procesamiento completo

#### **Lock (threading.Lock)**
- **Por qué**: Sincronizar salidas a consola
- **Problema resuelto**: Evita que textos de múltiples threads se mezclen
- **Uso**: Solo para secciones críticas (I/O)

#### **Poison Pill Pattern**
- **Por qué**: Forma limpia de detener threads
- **Implementación**: Enviar `None` a la cola señala fin de procesamiento
- **Ventaja**: Shutdown ordenado sin forzar terminación

---

### 3. Decisiones Específicas

#### **Número de Cocineros: 2 (configurable)**
- Balance entre concurrencia real y uso de recursos
- Fácil seguimiento en logs
- Suficiente para demostrar procesamiento paralelo

#### **daemon=True en Threads**
- Threads se cierran automáticamente con el programa principal
- Previene threads huérfanos que bloqueen el cierre

#### **timeout=1 en Queue.get()**
- Evita bloqueo indefinido
- Permite verificaciones periódicas del estado del thread
- Facilita shutdown limpio

#### **Intercalar Pedidos en Main**
```python
for i in range(3):
    pedido_h = creador_hamburguesas.crear_pedido(i)
    servicio.agregar_pedido(pedido_h)
    pedido_p = creador_pizzas.crear_pedido(i)
    servicio.agregar_pedido(pedido_p)
```
- Demuestra procesamiento concurrente real
- Los pedidos se mezclan en la salida según disponibilidad de cocineros

---

### 4. Principios SOLID Aplicados

- **S** (Single Responsibility): Cada clase tiene una responsabilidad única
- **O** (Open/Closed): Extensible sin modificar código existente
- **L** (Liskov Substitution): Subclases de `Pedido` son intercambiables
- **I** (Interface Segregation): Interfaces mínimas y específicas
- **D** (Dependency Inversion): Dependencias en abstracciones, no en clases concretas

---

### 5. Flujo de Ejecución

```
1. Main crea factories y pedidos → agregar_pedido()
2. ServicioPedidos.procesar_pedidos() crea pool de cocineros
3. Cada cocinero (thread) consume de la cola en paralelo
4. Queue.join() espera que todos los pedidos sean procesados
5. Poison pills (None) detienen cocineros
6. Thread.join() espera terminación limpia
7. Log final: "Todos los pedidos procesados"
```

---

### 6. Thread-Safety Garantizado

| Recurso Compartido | Mecanismo | Ubicación |
|-------------------|-----------|-----------|
| Cola de pedidos | `Queue` | `servicio_pedidos.py` |
| Salida a consola | `Lock` | `cocinero.py` |
| Contador de tareas | `task_done()` | `cocinero.py` |

---

## Extensibilidad Futura

Para agregar nuevos tipos de pedidos:
1. Crear clase `PedidoNuevo(Pedido)` en `pedido.py`
2. Crear `CreadorNuevo(CreadorPedidos)` en `factory.py`
3. Usar en `main.py` - **sin cambios en la lógica de procesamiento**

---

## Conclusión

El sistema implementa una arquitectura robusta, escalable y mantenible que:
- Procesa pedidos concurrentemente con múltiples threads
- Maneja sincronización correctamente sin race conditions
- Es fácilmente extensible con nuevos tipos de pedidos
- Sigue principios de diseño SOLID
- Usa patrones de diseño reconocidos y probados
