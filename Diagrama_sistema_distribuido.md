# Diagrama del Sistema Distribuido - PFO3

## Arquitectura Cliente-Servidor con Componentes Distribuidos

```mermaid
flowchart TB
    CM[📱 Cliente Móvil]
    CW[💻 Cliente Web]
    
    LB[⚖️ Load Balancer<br/>Nginx/HAProxy]
    
    W1[🔧 Worker 1<br/>Pool 5 hilos]
    W2[🔧 Worker 2<br/>Pool 5 hilos]
    W3[🔧 Worker 3<br/>Pool 5 hilos]
    
    RMQ[🐰 RabbitMQ<br/>Cola de Mensajes]
    
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

## 📋 Componentes del Sistema

### 1️⃣ Capa de Clientes
- **Cliente Móvil**: Aplicaciones iOS/Android
- **Cliente Web**: Aplicación en navegador
- **Protocolo**: HTTP/HTTPS o WebSocket

### 2️⃣ Capa de Balanceo
- **Load Balancer** (Nginx o HAProxy)
- **Puerto**: 80 (HTTP) / 443 (HTTPS)
- **Algoritmo**: Round Robin
- **Función**: Distribuir peticiones entre workers

### 3️⃣ Capa de Aplicación
- **Worker 1, 2, 3**: Servidores de procesamiento
- **Pool de Hilos**: 5 hilos por worker (15 tareas simultáneas)
- **Puertos**: 8001, 8002, 8003
- **Función**: Procesar lógica de negocio

### 4️⃣ Capa de Mensajería
- **RabbitMQ**: Sistema de cola de mensajes
- **Puerto**: 5672 (AMQP)
- **Patrón**: Publish/Subscribe
- **Función**: Comunicación asíncrona entre workers

### 5️⃣ Capa de Persistencia
- **PostgreSQL**: Base de datos relacional (Puerto 5432)
  - Datos estructurados (usuarios, pedidos, etc.)
- **Amazon S3**: Almacenamiento de archivos
  - Archivos grandes (imágenes, videos, PDFs)

---

## 🔄 Flujos de Operación

### Flujo 1: Petición Síncrona (Consulta simple)
```
Cliente → Load Balancer → Worker disponible → PostgreSQL → Respuesta
```

**Ejemplo**: Usuario hace login
1. Cliente envía credenciales
2. Load Balancer selecciona Worker 2 (menos carga)
3. Worker 2 consulta PostgreSQL
4. Worker 2 responde con token de sesión

### Flujo 2: Petición Asíncrona (Tarea pesada)
```
Cliente → LB → Worker 1 (respuesta inmediata)
Worker 1 → RabbitMQ (mensaje)
Worker 2 ← RabbitMQ (procesa mensaje)
Worker 2 → PostgreSQL/S3 (guarda resultado)
```

**Ejemplo**: Generar reporte mensual
1. Cliente solicita reporte
2. Worker 1 responde: "En proceso..."
3. Worker 1 envía tarea a RabbitMQ
4. Worker 3 procesa reporte en background
5. Worker 3 guarda PDF en S3
6. Sistema notifica al usuario (email/push)

### Flujo 3: Subida de Archivo
```
Cliente → LB → Worker → S3 (archivo) + PostgreSQL (metadata)
```

**Ejemplo**: Usuario sube foto de perfil
1. Cliente envía imagen
2. Worker 1 recibe archivo
3. Worker 1 sube a S3 → obtiene URL
4. Worker 1 guarda en PostgreSQL: {user_id, photo_url, size, date}
5. Worker 1 envía mensaje a RabbitMQ: "Generar thumbnails"
6. Worker 2 procesa thumbnails en background

---

## ⚡ Ventajas de esta Arquitectura

| Característica | Beneficio |
|----------------|-----------|
| **Alta Disponibilidad** | Si un worker falla, otros continúan |
| **Escalabilidad Horizontal** | Agregar más workers según demanda |
| **Procesamiento Paralelo** | 15 tareas simultáneas (3 workers × 5 hilos) |
| **Desacoplamiento** | Workers no dependen entre sí directamente |
| **Tolerancia a Fallos** | RabbitMQ garantiza entrega de mensajes |
| **Balanceo de Carga** | Distribución automática de peticiones |

---

## 🔧 Tecnologías y Puertos

| Componente | Tecnología | Puerto | Protocolo |
|------------|------------|--------|-----------|
| Load Balancer | Nginx/HAProxy | 80, 443 | HTTP/HTTPS |
| Workers | Python + Socket | 8001-8003 | TCP |
| Message Queue | RabbitMQ | 5672 | AMQP |
| Base de Datos | PostgreSQL | 5432 | PostgreSQL |
| File Storage | Amazon S3 | 443 | HTTPS |

---
