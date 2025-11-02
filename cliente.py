"""
Cliente que envía tareas al servidor
Permite enviar diferentes tipos de operaciones y recibir resultados
"""

import socket
import json
import time

class Cliente:
    def __init__(self, host='localhost', puerto=5000):
        self.host = host
        self.puerto = puerto
        
        print(f"[CLIENTE] Configurado para {host}:{puerto}")
    
    def enviar_tarea(self, operacion, datos):
        """Envía una tarea al servidor y retorna el resultado"""
        try:
            # Crear socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.puerto))
            
            # Preparar tarea
            tarea = {
                'operacion': operacion,
                'datos': datos
            }
            
            print(f"\n[ENVIANDO] {operacion} con datos: {datos}")
            
            # Enviar tarea
            tarea_json = json.dumps(tarea)
            sock.sendall(tarea_json.encode('utf-8'))
            
            # Recibir resultado
            data = sock.recv(4096).decode('utf-8')
            resultado = json.loads(data)
            
            # Mostrar resultado
            if resultado.get('estado') == 'completado':
                print(f"[RESULTADO] ✓ {resultado.get('resultado')}")
                print(f"[INFO] Procesado por: {resultado.get('worker', 'desconocido')}")
            elif resultado.get('estado') == 'error':
                print(f"[ERROR] ✗ {resultado.get('error')}")
            elif resultado.get('estado') == 'timeout':
                print(f"[TIMEOUT] ✗ {resultado.get('error')}")
            
            sock.close()
            return resultado
        
        except ConnectionRefusedError:
            print("[ERROR] No se pudo conectar al servidor. ¿Está ejecutándose?")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def menu_interactivo(self):
        """Menú interactivo para enviar tareas"""
        print("\n" + "="*60)
        print("CLIENTE DE TAREAS DISTRIBUIDAS")
        print("="*60)
        
        while True:
            print("\n--- OPERACIONES DISPONIBLES ---")
            print("1.  Suma")
            print("2.  Resta")
            print("3.  Multiplicación")
            print("4.  División")
            print("5.  Potencia")
            print("6.  Raíz cuadrada")
            print("7.  Factorial")
            print("8.  Verificar si es primo")
            print("9.  Fibonacci")
            print("10. Invertir texto")
            print("11. Convertir a mayúsculas")
            print("12. Contar palabras")
            print("13. Sleep (simular tarea larga)")
            print("14. Enviar múltiples tareas")
            print("0.  Salir")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '0':
                print("\n¡Hasta luego!")
                break
            
            elif opcion == '1':
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                self.enviar_tarea('suma', {'a': a, 'b': b})
            
            elif opcion == '2':
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                self.enviar_tarea('resta', {'a': a, 'b': b})
            
            elif opcion == '3':
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                self.enviar_tarea('multiplicacion', {'a': a, 'b': b})
            
            elif opcion == '4':
                a = float(input("Dividendo: "))
                b = float(input("Divisor: "))
                self.enviar_tarea('division', {'a': a, 'b': b})
            
            elif opcion == '5':
                base = float(input("Base: "))
                exponente = float(input("Exponente: "))
                self.enviar_tarea('potencia', {'base': base, 'exponente': exponente})
            
            elif opcion == '6':
                numero = float(input("Número: "))
                self.enviar_tarea('raiz', {'numero': numero})
            
            elif opcion == '7':
                n = int(input("Número: "))
                self.enviar_tarea('factorial', {'n': n})
            
            elif opcion == '8':
                n = int(input("Número: "))
                self.enviar_tarea('primo', {'n': n})
            
            elif opcion == '9':
                n = int(input("Posición (n): "))
                self.enviar_tarea('fibonacci', {'n': n})
            
            elif opcion == '10':
                texto = input("Texto: ")
                self.enviar_tarea('inverso_texto', {'texto': texto})
            
            elif opcion == '11':
                texto = input("Texto: ")
                self.enviar_tarea('mayusculas', {'texto': texto})
            
            elif opcion == '12':
                texto = input("Texto: ")
                self.enviar_tarea('contar_palabras', {'texto': texto})
            
            elif opcion == '13':
                segundos = int(input("Segundos a dormir: "))
                self.enviar_tarea('sleep', {'segundos': segundos})
            
            elif opcion == '14':
                self.enviar_multiples_tareas()
            
            else:
                print("Opción no válida")
            
            input("\nPresiona Enter para continuar...")
    
    def enviar_multiples_tareas(self):
        """Envía múltiples tareas para demostrar el procesamiento paralelo"""
        print("\n[DEMO] Enviando múltiples tareas...")
        
        tareas = [
            ('suma', {'a': 10, 'b': 20}),
            ('multiplicacion', {'a': 5, 'b': 7}),
            ('factorial', {'n': 10}),
            ('primo', {'n': 97}),
            ('fibonacci', {'n': 15}),
            ('mayusculas', {'texto': 'hola mundo'}),
        ]
        
        inicio = time.time()
        
        for operacion, datos in tareas:
            self.enviar_tarea(operacion, datos)
            time.sleep(0.5)  # Pequeña pausa entre tareas
        
        fin = time.time()
        
        print(f"\n[INFO] {len(tareas)} tareas enviadas en {fin - inicio:.2f} segundos")
    
    def demo_automatica(self):
        """Ejecuta una demostración automática"""
        print("\n[DEMO] Ejecutando demostración automática...")
        
        demos = [
            ('suma', {'a': 15, 'b': 27}, "Suma: 15 + 27"),
            ('multiplicacion', {'a': 12, 'b': 8}, "Multiplicación: 12 × 8"),
            ('potencia', {'base': 2, 'exponente': 10}, "Potencia: 2^10"),
            ('factorial', {'n': 6}, "Factorial: 6!"),
            ('primo', {'n': 17}, "¿Es primo?: 17"),
            ('fibonacci', {'n': 10}, "Fibonacci: posición 10"),
            ('inverso_texto', {'texto': 'Python'}, "Invertir: 'Python'"),
        ]
        
        for operacion, datos, descripcion in demos:
            print(f"\n→ {descripcion}")
            self.enviar_tarea(operacion, datos)
            time.sleep(1)
        
        print("\n[DEMO] Demostración completada")

if __name__ == '__main__':
    import sys
    
    cliente = Cliente()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        cliente.demo_automatica()
    else:
        cliente.menu_interactivo()
