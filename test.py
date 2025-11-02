"""
Script de prueba para demostrar el sistema de distribución de tareas
Este script ejecuta pruebas de ejemplo sin necesidad de interacción
"""

import socket
import json
import time

def enviar_tarea(operacion, datos, host='localhost', puerto=5000):
    """Envía una tarea y retorna el resultado"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, puerto))
        
        tarea = {
            'operacion': operacion,
            'datos': datos
        }
        
        sock.sendall(json.dumps(tarea).encode('utf-8'))
        data = sock.recv(4096).decode('utf-8')
        resultado = json.loads(data)
        
        sock.close()
        return resultado
    except Exception as e:
        return {'error': str(e), 'estado': 'fallo_conexion'}

def test_operaciones_matematicas():
    """Prueba operaciones matemáticas básicas"""
    print("\n" + "="*60)
    print("TEST 1: Operaciones Matemáticas")
    print("="*60)
    
    tests = [
        ('suma', {'a': 15, 'b': 27}, 42),
        ('resta', {'a': 50, 'b': 18}, 32),
        ('multiplicacion', {'a': 7, 'b': 8}, 56),
        ('division', {'a': 100, 'b': 4}, 25),
        ('potencia', {'base': 2, 'exponente': 8}, 256),
    ]
    
    for operacion, datos, esperado in tests:
        resultado = enviar_tarea(operacion, datos)
        
        if resultado.get('estado') == 'completado':
            obtenido = resultado.get('resultado')
            status = "✓ PASS" if obtenido == esperado else "✗ FAIL"
            print(f"{status} | {operacion}({datos}) = {obtenido} (esperado: {esperado})")
            if resultado.get('worker'):
                print(f"      Worker: {resultado['worker']}")
        else:
            print(f"✗ ERROR | {operacion} - {resultado.get('error', 'desconocido')}")
        
        time.sleep(0.2)

def test_operaciones_numericas():
    """Prueba operaciones numéricas avanzadas"""
    print("\n" + "="*60)
    print("TEST 2: Operaciones Numéricas Avanzadas")
    print("="*60)
    
    tests = [
        ('raiz', {'numero': 144}, 12),
        ('factorial', {'n': 5}, 120),
        ('primo', {'n': 17}, True),
        ('primo', {'n': 18}, False),
        ('fibonacci', {'n': 10}, 55),
    ]
    
    for operacion, datos, esperado in tests:
        resultado = enviar_tarea(operacion, datos)
        
        if resultado.get('estado') == 'completado':
            obtenido = resultado.get('resultado')
            status = "✓ PASS" if obtenido == esperado else "✗ FAIL"
            print(f"{status} | {operacion}({datos}) = {obtenido} (esperado: {esperado})")
            if resultado.get('worker'):
                print(f"      Worker: {resultado['worker']}")
        else:
            print(f"✗ ERROR | {operacion} - {resultado.get('error', 'desconocido')}")
        
        time.sleep(0.2)

def test_operaciones_texto():
    """Prueba operaciones de texto"""
    print("\n" + "="*60)
    print("TEST 3: Operaciones de Texto")
    print("="*60)
    
    tests = [
        ('inverso_texto', {'texto': 'Python'}, 'nohtyP'),
        ('mayusculas', {'texto': 'hola mundo'}, 'HOLA MUNDO'),
        ('contar_palabras', {'texto': 'uno dos tres'}, 3),
    ]
    
    for operacion, datos, esperado in tests:
        resultado = enviar_tarea(operacion, datos)
        
        if resultado.get('estado') == 'completado':
            obtenido = resultado.get('resultado')
            status = "✓ PASS" if obtenido == esperado else "✗ FAIL"
            print(f"{status} | {operacion}({datos}) = {obtenido}")
            if resultado.get('worker'):
                print(f"      Worker: {resultado['worker']}")
        else:
            print(f"✗ ERROR | {operacion} - {resultado.get('error', 'desconocido')}")
        
        time.sleep(0.2)

def test_manejo_errores():
    """Prueba el manejo de errores"""
    print("\n" + "="*60)
    print("TEST 4: Manejo de Errores")
    print("="*60)
    
    tests = [
        ('division', {'a': 10, 'b': 0}, "División por cero"),
        ('raiz', {'numero': -4}, "raíz de número negativo"),
        ('operacion_invalida', {'x': 1}, "Operación desconocida"),
    ]
    
    for operacion, datos, error_esperado in tests:
        resultado = enviar_tarea(operacion, datos)
        
        if resultado.get('estado') == 'error':
            error = resultado.get('error', '')
            tiene_error = any(palabra in error.lower() for palabra in error_esperado.lower().split())
            status = "✓ PASS" if tiene_error else "✗ FAIL"
            print(f"{status} | {operacion} - Error capturado: {error}")
        else:
            print(f"✗ FAIL | {operacion} - Debería haber generado error")
        
        time.sleep(0.2)

def test_carga_paralela():
    """Prueba envío de múltiples tareas en paralelo"""
    print("\n" + "="*60)
    print("TEST 5: Carga Paralela (10 tareas)")
    print("="*60)
    
    import threading
    
    tareas = [
        ('suma', {'a': i, 'b': i*2})
        for i in range(10)
    ]
    
    resultados = []
    inicio = time.time()
    
    def ejecutar_tarea(idx, op, datos):
        res = enviar_tarea(op, datos)
        resultados.append((idx, res))
    
    threads = []
    for idx, (op, datos) in enumerate(tareas):
        t = threading.Thread(target=ejecutar_tarea, args=(idx, op, datos))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    fin = time.time()
    tiempo_total = fin - inicio
    
    completadas = sum(1 for _, r in resultados if r.get('estado') == 'completado')
    print(f"\n✓ Completadas: {completadas}/{len(tareas)}")
    print(f"✓ Tiempo total: {tiempo_total:.2f} segundos")
    print(f"✓ Promedio por tarea: {tiempo_total/len(tareas):.2f} segundos")
    
    # Mostrar distribución de workers
    workers = {}
    for _, res in resultados:
        if res.get('worker'):
            worker = res['worker']
            workers[worker] = workers.get(worker, 0) + 1
    
    if workers:
        print(f"\n✓ Distribución de tareas por worker:")
        for worker, count in workers.items():
            print(f"  - {worker}: {count} tareas")

def verificar_servidor():
    """Verifica si el servidor está en ejecución"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(('localhost', 5000))
        sock.close()
        return True
    except:
        return False

def main():
    print("\n" + "="*60)
    print("SUITE DE PRUEBAS - SISTEMA DE DISTRIBUCIÓN DE TAREAS")
    print("="*60)
    
    # Verificar servidor
    print("\nVerificando servidor...")
    if not verificar_servidor():
        print("❌ ERROR: El servidor no está en ejecución")
        print("\nPor favor ejecuta primero:")
        print("  1. python3 servidor.py")
        print("  2. python3 worker.py (en otra terminal)")
        print("  3. python3 test.py")
        return
    
    print("✓ Servidor detectado")
    time.sleep(1)
    
    # Ejecutar tests
    try:
        test_operaciones_matematicas()
        test_operaciones_numericas()
        test_operaciones_texto()
        test_manejo_errores()
        test_carga_paralela()
        
        print("\n" + "="*60)
        print("RESUMEN: Todos los tests completados")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Tests cancelados por el usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == '__main__':
    main()
