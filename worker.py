"""
Worker que procesa tareas
Se conecta al servidor y procesa las tareas que recibe
"""

import socket
import json
import time
import math

class Worker:
    def __init__(self, host='localhost', puerto=5001, nombre=None):
        self.host = host
        self.puerto = puerto
        self.nombre = nombre or f"Worker-{id(self)}"
        self.sock = None
        
        print(f"[{self.nombre}] Inicializado")
    
    def procesar_tarea(self, tarea):
        """Procesa una tarea y retorna el resultado"""
        operacion = tarea.get('operacion')
        datos = tarea.get('datos', {})
        tarea_id = tarea.get('id')
        
        print(f"[{self.nombre}] Procesando tarea {tarea_id}: {operacion}")
        
        try:
            resultado = None
            
            if operacion == 'suma':
                a = datos.get('a', 0)
                b = datos.get('b', 0)
                resultado = a + b
            
            elif operacion == 'resta':
                a = datos.get('a', 0)
                b = datos.get('b', 0)
                resultado = a - b
            
            elif operacion == 'multiplicacion':
                a = datos.get('a', 0)
                b = datos.get('b', 0)
                resultado = a * b
            
            elif operacion == 'division':
                a = datos.get('a', 0)
                b = datos.get('b', 1)
                if b == 0:
                    raise ValueError("División por cero")
                resultado = a / b
            
            elif operacion == 'potencia':
                base = datos.get('base', 0)
                exponente = datos.get('exponente', 1)
                resultado = base ** exponente
            
            elif operacion == 'raiz':
                numero = datos.get('numero', 0)
                if numero < 0:
                    raise ValueError("No se puede calcular raíz de número negativo")
                resultado = math.sqrt(numero)
            
            elif operacion == 'factorial':
                n = datos.get('n', 0)
                if n < 0:
                    raise ValueError("Factorial no definido para negativos")
                resultado = math.factorial(n)
            
            elif operacion == 'primo':
                n = datos.get('n', 2)
                resultado = self.es_primo(n)
            
            elif operacion == 'fibonacci':
                n = datos.get('n', 0)
                resultado = self.fibonacci(n)
            
            elif operacion == 'inverso_texto':
                texto = datos.get('texto', '')
                resultado = texto[::-1]
            
            elif operacion == 'mayusculas':
                texto = datos.get('texto', '')
                resultado = texto.upper()
            
            elif operacion == 'contar_palabras':
                texto = datos.get('texto', '')
                resultado = len(texto.split())
            
            elif operacion == 'sleep':
                segundos = datos.get('segundos', 1)
                time.sleep(segundos)
                resultado = f"Dormido por {segundos} segundos"
            
            else:
                raise ValueError(f"Operación desconocida: {operacion}")
            
            # Simular tiempo de procesamiento
            time.sleep(0.1)
            
            return {
                'id': tarea_id,
                'operacion': operacion,
                'resultado': resultado,
                'estado': 'completado',
                'worker': self.nombre
            }
        
        except Exception as e:
            return {
                'id': tarea_id,
                'operacion': operacion,
                'error': str(e),
                'estado': 'error',
                'worker': self.nombre
            }
    
    def es_primo(self, n):
        """Verifica si un número es primo"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def fibonacci(self, n):
        """Calcula el n-ésimo número de Fibonacci"""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def conectar(self):
        """Conecta al servidor"""
        print(f"[{self.nombre}] Conectando a {self.host}:{self.puerto}")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.puerto))
        
        print(f"[{self.nombre}] Conectado al servidor")
    
    def trabajar(self):
        """Loop principal del worker"""
        try:
            while True:
                # Recibir tarea del servidor
                data = self.sock.recv(4096).decode('utf-8') # type: ignore
                
                if not data:
                    print(f"[{self.nombre}] Servidor desconectado")
                    break
                
                tarea = json.loads(data)
                
                # Procesar tarea
                resultado = self.procesar_tarea(tarea)
                
                # Enviar resultado
                resultado_json = json.dumps(resultado)
                self.sock.sendall(resultado_json.encode('utf-8')) # type: ignore
                
                print(f"[{self.nombre}] Tarea {tarea['id']} completada")
        
        except Exception as e:
            print(f"[{self.nombre}] Error: {e}")
        
        finally:
            if self.sock:
                self.sock.close()
            print(f"[{self.nombre}] Desconectado")
    
    def iniciar(self):
        """Inicia el worker"""
        try:
            self.conectar()
            self.trabajar()
        except KeyboardInterrupt:
            print(f"\n[{self.nombre}] Detenido por usuario")
        except Exception as e:
            print(f"[{self.nombre}] Error: {e}")

if __name__ == '__main__':
    import sys
    
    nombre = None
    if len(sys.argv) > 1:
        nombre = sys.argv[1]
    
    worker = Worker(nombre=nombre)
    worker.iniciar()
