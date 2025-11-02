# Diagrama del Sistema Distribuido - PFO3

## Arquitectura Cliente-Servidor con Componentes Distribuidos

```mermaid
graph TB
    subgraph "Capa de Clientes"
        CM[📱 Cliente MóviliOS/Android]
        CW[💻 Cliente WebBrowser]
    end
    
    subgraph "Capa de Balanceo"
        LB[⚖️ Load BalancerNginx/HAProxyPuerto: 80/443]
    end
    
    subgraph "Capa de Aplicación"
        W1[🔧 Worker 1Pool: 5 hilosPuerto: 8001]
        W2[🔧 Worker 2Pool: 5 hilosPuerto: 8002]
        W3[🔧 Worker 3Pool: 5 hilosPuerto: 8003]
    end
    
    subgraph "Capa de Mensajería"
        RMQ[🐰 RabbitMQCola de MensajesPuerto: 5672]
    end
    
    subgraph "Capa de Persistencia"
        PG[(🐘 PostgreSQLBase de DatosPuerto: 5432)]
        S3[☁️ Amazon S3Almacenamientode Archivos]
    end
    
    %% Conexiones de Clientes a Load Balancer
    CM -->|HTTP/WebSocket| LB
    CW -->|HTTP/WebSocket| LB
    
    %% Conexiones de Load Balancer a Workers
    LB -->|Round Robin| W1
    LB -->|Round Robin| W2
    LB -->|Round Robin| W3
    
    %% Conexiones de Workers a RabbitMQ
    W1 |Pub/Sub| RMQ
    W2 |Pub/Sub| RMQ
    W3 |Pub/Sub| RMQ
    
    %% Conexiones de Workers a Bases de Datos
    W1 -->|SQL Queries| PG
    W2 -->|SQL Queries| PG
    W3 -->|SQL Queries| PG
    
    W1 -->|Upload/Download| S3
    W2 -->|Upload/Download| S3
    W3 -->|Upload/Download| S3
    
    %% Estilos
    classDef clientStyle fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    classDef lbStyle fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    classDef workerStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef mqStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef dbStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class CM,CW clientStyle
    class LB lbStyle
    class W1,W2,W3 workerStyle
    class RMQ mqStyle
    class PG,S3 dbStyle
```

## 📋 Descripción de Flujo

### 1. **Flujo de una Petición Típica:**
```
Cliente → Load Balancer → Worker disponible → Base de Datos → Respuesta al Cliente
```

### 2. **Flujo de una Tarea Asíncrona:**
```
Cliente → Load Balancer → Worker 1 → RabbitMQ (mensaje) → Worker 2 procesa → Base de Datos
```

### 3. **Flujo de Subida de Archivo:**
```
Cliente → Load Balancer → Worker → S3 (archivo) + PostgreSQL (metadata)
```

---

## 🔧 Características Clave del Sistema

### **Alta Disponibilidad**
- Si un worker falla, el Load Balancer redirige a otro
- La cola RabbitMQ garantiza que las tareas no se pierdan

### **Escalabilidad Horizontal**
- Se pueden agregar más workers según la demanda
- El Load Balancer distribuye automáticamente la carga

### **Desacoplamiento**
- Los workers se comunican vía RabbitMQ sin conocerse directamente
- Facilita el mantenimiento y las actualizaciones

### **Pool de Hilos por Worker**
- Cada worker puede procesar múltiples tareas simultáneamente
- Ejemplo: Worker con 5 hilos = 5 tareas en paralelo

---

## 🌐 Puertos Estándar Utilizados

| Componente | Puerto | Protocolo |
|------------|--------|-----------|
| Nginx/HAProxy | 80, 443 | HTTP/HTTPS |
| Workers | 8001-8003 | TCP/HTTP |
| RabbitMQ | 5672 | AMQP |
| PostgreSQL | 5432 | PostgreSQL Protocol |
| S3 | 443 | HTTPS |

---

## 💡 Ventajas de esta Arquitectura

1. **Tolerancia a Fallos**: Si un componente falla, el sistema sigue funcionando
2. **Escalabilidad**: Fácil agregar más recursos según demanda
3. **Mantenimiento**: Se pueden actualizar workers sin detener el servicio
4. **Performance**: Procesamiento paralelo mediante múltiples workers e hilos
5. **Flexibilidad**: Diferentes tipos de almacenamiento según necesidad

---