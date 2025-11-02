# Sistema de Distribución de Tareas con Sockets

Sistema cliente-servidor en Python para distribuir tareas a múltiples workers usando sockets TCP.

## Arquitectura

```
┌─────────┐      Tareas       ┌──────────┐      Tareas      ┌─────────┐
│ Cliente │ ─────────────────> │ Servidor │ ───────────────> │ Worker1 │
└─────────┘                    └──────────┘                  └─────────┘
                                    │                        ┌─────────┐
                                    └───────────────────────>│ Worker2 │
                                                             └─────────┘
```

## Componentes

### 1. Servidor (`servidor.py`)
- **Puerto 5000**: Escucha conexiones de clientes
- **Puerto 5001**: Escucha conexiones de workers
- Distribuye tareas a workers disponibles
- Retorna resultados a los clientes

### 2. Worker (`worker.py`)
- Se conecta al servidor
- Procesa tareas recibidas
- Soporta operaciones:
  - Matemáticas: suma, resta, multiplicación, división, potencia, raíz, factorial
  - Números: verificar primos, Fibonacci
  - Texto: invertir, mayúsculas, contar palabras
  - Utilidad: sleep (simulación)

### 3. Cliente (`cliente.py`)
- Envía tareas al servidor
- Recibe y muestra resultados
- Menú interactivo o modo demo

## Instalación

No requiere dependencias externas, solo Python 3.6+

```bash
# Clonar o descargar los archivos
# servidor.py
# worker.py
# cliente.py
```

## Uso

### Paso 1: Iniciar el Servidor

```bash
python3 servidor.py
```

Salida esperada:
```
[SERVIDOR] Inicializado en localhost
[SERVIDOR] Puerto clientes: 5000
[SERVIDOR] Puerto workers: 5001
[SERVIDOR] Escuchando clientes en puerto 5000
[SERVIDOR] Escuchando workers en puerto 5001
[SERVIDOR] Listo para recibir conexiones
```

### Paso 2: Iniciar Workers

Abre nuevas terminales y ejecuta uno o más workers:

```bash
# Terminal 2
python3 worker.py Worker-A

# Terminal 3
python3 worker.py Worker-B

# Terminal 4 (opcional)
python3 worker.py Worker-C
```

Salida esperada por worker:
```
[Worker-A] Inicializado
[Worker-A] Conectando a localhost:5001
[Worker-A] Conectado al servidor
```

### Paso 3: Ejecutar Cliente

#### Modo Interactivo
```bash
python3 cliente.py
```

Menú de opciones:
```
--- OPERACIONES DISPONIBLES ---
1.  Suma
2.  Resta
3.  Multiplicación
4.  División
5.  Potencia
6.  Raíz cuadrada
7.  Factorial
8.  Verificar si es primo
9.  Fibonacci
10. Invertir texto
11. Convertir a mayúsculas
12. Contar palabras
13. Sleep (simular tarea larga)
14. Enviar múltiples tareas
0.  Salir
```

#### Modo Demo
```bash
python3 cliente.py --demo
```

Ejecuta automáticamente varias tareas de ejemplo.

## Ejemplos de Uso

### Ejemplo 1: Operación Simple

**Cliente:**
```
Selecciona una opción: 1
Primer número: 25
Segundo número: 17
```

**Salida:**
```
[ENVIANDO] suma con datos: {'a': 25.0, 'b': 17.0}
[RESULTADO] ✓ 42.0
[INFO] Procesado por: Worker-A
```

### Ejemplo 2: Múltiples Tareas

El cliente puede enviar múltiples tareas que se distribuyen automáticamente entre workers:

```
Selecciona una opción: 14
[DEMO] Enviando múltiples tareas...

[ENVIANDO] suma con datos: {'a': 10, 'b': 20}
[RESULTADO] ✓ 30
[INFO] Procesado por: Worker-A

[ENVIANDO] multiplicacion con datos: {'a': 5, 'b': 7}
[RESULTADO] ✓ 35
[INFO] Procesado por: Worker-B

...
```

### Ejemplo 3: Procesamiento de Texto

```
Selecciona una opción: 10
Texto: Python
[ENVIANDO] inverso_texto con datos: {'texto': 'Python'}
[RESULTADO] ✓ nohtyP
[INFO] Procesado por: Worker-A
```

## Características

### ✅ Implementadas

- **Comunicación por sockets TCP**
- **Distribución automática de tareas**
- **Múltiples workers concurrentes**
- **Cola de tareas con queue.Queue**
- **Threading para manejar múltiples conexiones**
- **Manejo de errores y timeouts**
- **IDs únicos para cada tarea**
- **13+ tipos de operaciones**

### 🔧 Arquitectura Técnica

- **JSON** para serialización de datos
- **Threading** para concurrencia
- **Queue** para sincronización segura
- **Lock** para secciones críticas
- **Timeout de 30 segundos** por tarea

## Flujo de Trabajo

1. Cliente crea tarea y se conecta al servidor (puerto 5000)
2. Servidor asigna ID único a la tarea
3. Servidor agrega tarea a cola de tareas
4. Worker disponible toma tarea de la cola
5. Worker procesa tarea y retorna resultado al servidor
6. Servidor envía resultado al cliente
7. Cliente muestra resultado

## Escalabilidad

El sistema soporta:
- ✅ Múltiples clientes simultáneos
- ✅ Múltiples workers simultáneos
- ✅ Cola ilimitada de tareas (limitada por memoria)
- ✅ Procesamiento paralelo de tareas

## Pruebas

### Test de Carga Básico

```bash
# Terminal 1: Servidor
python3 servidor.py

# Terminales 2-4: Workers
python3 worker.py Worker-1
python3 worker.py Worker-2
python3 worker.py Worker-3

# Terminales 5-7: Clientes
python3 cliente.py --demo &
python3 cliente.py --demo &
python3 cliente.py --demo &
```

## Manejo de Errores

El sistema maneja:
- División por cero
- Números negativos en operaciones no permitidas
- Workers desconectados
- Timeout de tareas
- Operaciones desconocidas
- Errores de red

## Limitaciones Actuales

- No hay persistencia de tareas
- No hay reintentos automáticos
- Workers deben reiniciarse manualmente si fallan
- No hay autenticación
- Comunicación no encriptada

## Posibles Mejoras

1. **Persistencia**: Guardar tareas en base de datos
2. **Heartbeat**: Monitoreo de salud de workers
3. **Prioridades**: Cola de prioridad para tareas urgentes
4. **Autenticación**: Tokens para clientes y workers
5. **Encriptación**: SSL/TLS para comunicación segura
6. **Dashboard**: Interfaz web para monitoreo
7. **Métricas**: Estadísticas de rendimiento
8. **Retry logic**: Reintentos automáticos en caso de fallo

## Estructura de Mensajes

### Tarea (Cliente → Servidor)
```json
{
    "operacion": "suma",
    "datos": {
        "a": 10,
        "b": 20
    }
}
```

### Tarea con ID (Servidor → Worker)
```json
{
    "id": 1,
    "operacion": "suma",
    "datos": {"a": 10, "b": 20},
    "timestamp": "2025-11-02T10:30:00"
}
```

### Resultado (Worker → Servidor → Cliente)
```json
{
    "id": 1,
    "operacion": "suma",
    "resultado": 30,
    "estado": "completado",
    "worker": "Worker-A"
}
```

## Licencia

Código de ejemplo educativo. Libre para uso y modificación.