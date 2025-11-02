"""
Servidor de distribución de tareas
Recibe tareas de clientes y las distribuye a workers disponibles
"""

import socket
import threading
import json
import queue
import time
from datetime import datetime

class ServidorTareas:
    def __init__(self, host='localhost', puerto_clientes=5000, puerto_workers=5001):
        self.host = host
        self.puerto_clientes = puerto_clientes
        self.puerto_workers = puerto_workers
        
        # Colas para manejar tareas y resultados
        self.cola_tareas = queue.Queue()
        self.resultados = {}
        self.lock_resultados = threading.Lock()
        
        # Lista de workers disponibles
        self.workers_disponibles = queue.Queue()
        self.workers_conectados = []
        self.lock_workers = threading.Lock()
        
        # Control de tareas
        self.tarea_id = 0
        self.lock_tarea_id = threading.Lock()
        
        # Mapeo de tarea_id a socket del cliente
        self.clientes_esperando = {}
        self.lock_clientes = threading.Lock()
        
        print(f"[SERVIDOR] Inicializado en {host}")
        print(f"[SERVIDOR] Puerto clientes: {puerto_clientes}")
        print(f"[SERVIDOR] Puerto workers: {puerto_workers}")
    
    def obtener_tarea_id(self):
        """Genera un ID único para cada tarea"""
        with self.lock_tarea_id:
            self.tarea_id += 1
            return self.tarea_id
    
    def manejar_cliente(self, conn, addr):
        """Maneja la conexión de un cliente que envía tareas"""
        print(f"[CLIENTE] Conectado desde {addr}")
        
        try:
            # Recibir datos del cliente
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
            
            tarea = json.loads(data)
            tarea_id = self.obtener_tarea_id()
            tarea['id'] = tarea_id
            tarea['timestamp'] = datetime.now().isoformat()
            
            print(f"[TAREA {tarea_id}] Recibida: {tarea.get('operacion', 'desconocida')}")
            
            # Registrar cliente esperando resultado
            with self.lock_clientes:
                self.clientes_esperando[tarea_id] = conn
            
            # Agregar tarea a la cola
            self.cola_tareas.put(tarea)
            
            # Esperar resultado (con timeout)
            tiempo_espera = 0
            max_espera = 30  # 30 segundos máximo
            
            while tiempo_espera < max_espera:
                with self.lock_resultados:
                    if tarea_id in self.resultados:
                        resultado = self.resultados.pop(tarea_id)
                        respuesta = json.dumps(resultado)
                        conn.sendall(respuesta.encode('utf-8'))
                        print(f"[TAREA {tarea_id}] Resultado enviado al cliente")
                        break
                
                time.sleep(0.1)
                tiempo_espera += 0.1
            else:
                # Timeout
                error = {
                    'id': tarea_id,
                    'error': 'Timeout: no hay workers disponibles',
                    'estado': 'timeout'
                }
                conn.sendall(json.dumps(error).encode('utf-8'))
                print(f"[TAREA {tarea_id}] Timeout - no procesada")
        
        except Exception as e:
            print(f"[ERROR] Manejando cliente: {e}")
        
        finally:
            with self.lock_clientes:
                if tarea_id in self.clientes_esperando:
                    del self.clientes_esperando[tarea_id]
            conn.close()
    
    def manejar_worker(self, conn, addr):
        """Maneja la conexión de un worker que procesa tareas"""
        print(f"[WORKER] Conectado desde {addr}")
        
        with self.lock_workers:
            self.workers_conectados.append(addr)
        
        try:
            while True:
                # Worker está disponible, agregar a la cola
                self.workers_disponibles.put(conn)
                
                # Esperar por una tarea
                try:
                    tarea = self.cola_tareas.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Sacar worker de la cola de disponibles
                try:
                    self.workers_disponibles.get_nowait()
                except queue.Empty:
                    pass
                
                # Enviar tarea al worker
                tarea_json = json.dumps(tarea)
                conn.sendall(tarea_json.encode('utf-8'))
                print(f"[TAREA {tarea['id']}] Enviada a worker {addr}")
                
                # Recibir resultado del worker
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    print(f"[WORKER] {addr} desconectado")
                    break
                
                resultado = json.loads(data)
                tarea_id = resultado.get('id')
                
                # Guardar resultado
                with self.lock_resultados:
                    self.resultados[tarea_id] = resultado
                
                print(f"[TAREA {tarea_id}] Resultado recibido de worker {addr}")
        
        except Exception as e:
            print(f"[ERROR] Worker {addr}: {e}")
        
        finally:
            with self.lock_workers:
                if addr in self.workers_conectados:
                    self.workers_conectados.remove(addr)
            conn.close()
            print(f"[WORKER] {addr} desconectado")
    
    def aceptar_clientes(self):
        """Acepta conexiones de clientes"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.puerto_clientes))
        sock.listen(5)
        
        print(f"[SERVIDOR] Escuchando clientes en puerto {self.puerto_clientes}")
        
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=self.manejar_cliente, args=(conn, addr))
            thread.daemon = True
            thread.start()
    
    def aceptar_workers(self):
        """Acepta conexiones de workers"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.puerto_workers))
        sock.listen(5)
        
        print(f"[SERVIDOR] Escuchando workers en puerto {self.puerto_workers}")
        
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=self.manejar_worker, args=(conn, addr))
            thread.daemon = True
            thread.start()
    
    def iniciar(self):
        """Inicia el servidor"""
        print("[SERVIDOR] Iniciando...")
        
        # Thread para aceptar clientes
        thread_clientes = threading.Thread(target=self.aceptar_clientes)
        thread_clientes.daemon = True
        thread_clientes.start()
        
        # Thread para aceptar workers
        thread_workers = threading.Thread(target=self.aceptar_workers)
        thread_workers.daemon = True
        thread_workers.start()
        
        print("[SERVIDOR] Listo para recibir conexiones")
        print("Presiona Ctrl+C para detener")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Deteniendo...")

if __name__ == '__main__':
    servidor = ServidorTareas()
    servidor.iniciar()
