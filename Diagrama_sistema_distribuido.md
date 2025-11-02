# Diagrama del Sistema Distribuido - PFO3

## Arquitectura Cliente-Servidor con Componentes Distribuidos

```mermaid
flowchart TB
    CM[📱 Cliente Móvil]
    CW[💻 Cliente Web]
    
    LB[⚖️ Load BalancerNginx/HAProxy]
    
    W1[🔧 Worker 1Pool 5 hilos]
    W2[🔧 Worker 2Pool 5 hilos]
    W3[🔧 Worker 3Pool 5 hilos]
    
    RMQ[🐰 RabbitMQCola de Mensajes]
    
    PG[(🐘 PostgreSQL)]
    S3[☁️ Amazon S3]
    
    CM -->|HTTP| LB
    CW -->|HTTP| LB
    
    LB -->|Round Robin| W1
    LB -->|Round Robin| W2
    LB -->|Round Robin| W3
    
    W1 -.->|Pub/Sub| RMQ
    W2 -.->|Pub/Sub| RMQ
    W3 -.->|Pub/Sub| RMQ
    
    W1 -->|SQL| PG
    W2 -->|SQL| PG
    W3 -->|SQL| PG
    
    W1 -->|Files| S3
    W2 -->|Files| S3
    W3 -->|Files| S3
    
    style CM fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style CW fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style LB fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style W1 fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style W2 fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style W3 fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style RMQ fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style PG fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style S3 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

---

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