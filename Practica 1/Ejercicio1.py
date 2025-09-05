def resolver_puente(tiempos):
    """
    Resuelve el problema del puente usando DFS con poda.
    
    Args:
        tiempos: Lista de tiempos que tarda cada persona en cruzar
    
    Returns:
        Tupla con (tiempo_minimo, lista_de_movimientos)
    """
    n = len(tiempos)
    mejor_tiempo = float('inf')
    mejor_solucion = []
    
    def dfs(personas_der, antorcha_der, tiempo_actual, camino, profundidad):
        nonlocal mejor_tiempo, mejor_solucion
        
        # Poda por tiempo
        if tiempo_actual >= mejor_tiempo:
            return
            
        # Poda por profundidad excesiva (evita ciclos infinitos)
        if profundidad > 2 * n:
            return
        
        # Objetivo alcanzado - todos en la derecha
        if personas_der == (1 << n) - 1:
            if tiempo_actual < mejor_tiempo:
                mejor_tiempo = tiempo_actual
                mejor_solucion = camino.copy()
            return
        
        # Obtener personas en cada lado
        personas_izq = [i for i in range(n) if not (personas_der & (1 << i))]
        personas_derecha = [i for i in range(n) if (personas_der & (1 << i))]
        
        if antorcha_der:  # Antorcha en derecha - regresa 1 persona
            for persona in personas_derecha:
                nuevo_der = personas_der & ~(1 << persona)
                nuevo_tiempo = tiempo_actual + tiempos[persona]
                nuevo_camino = camino + [f"P{persona+1}({tiempos[persona]}) ←"]
                
                dfs(nuevo_der, False, nuevo_tiempo, nuevo_camino, profundidad + 1)
        
        else:  # Antorcha en izquierda - pueden cruzar 1 o 2 personas
            # 1 persona
            for persona in personas_izq:
                nuevo_der = personas_der | (1 << persona)
                nuevo_tiempo = tiempo_actual + tiempos[persona]
                nuevo_camino = camino + [f"P{persona+1}({tiempos[persona]}) →"]
                
                dfs(nuevo_der, True, nuevo_tiempo, nuevo_camino, profundidad + 1)
            
            # 2 personas
            for i in range(len(personas_izq)):
                for j in range(i + 1, len(personas_izq)):
                    p1, p2 = personas_izq[i], personas_izq[j]
                    nuevo_der = personas_der | (1 << p1) | (1 << p2)
                    tiempo_mov = max(tiempos[p1], tiempos[p2])
                    nuevo_tiempo = tiempo_actual + tiempo_mov
                    nuevo_camino = camino + [f"(P{p1+1}({tiempos[p1]}), P{p2+1}({tiempos[p2]})) →"]
                    
                    dfs(nuevo_der, True, nuevo_tiempo, nuevo_camino, profundidad + 1)
    
    # Iniciar búsqueda: nadie en derecha, antorcha en izquierda, profundidad 0
    dfs(0, False, 0, [], 0)
    return mejor_tiempo, mejor_solucion

def mostrar_solucion(tiempos, tiempo_minimo, movimientos):
    """Muestra la solución de forma clara"""
    print("=" * 50)
    print("SOLUCIÓN ÓPTIMA")
    print("=" * 50)
    
    if not movimientos:
        print("No se encontró solución")
        return
    
    tiempo_acumulado = 0
    for i, movimiento in enumerate(movimientos, 1):
        # Verificar si es tupla o string
        if isinstance(movimiento, tuple):
            desc, tiempo = movimiento
        else:
            # Si es string, intentar extraer el tiempo
            desc = movimiento
            try:
                if "←" in movimiento:
                    tiempo = int(movimiento.split("(")[1].split(")")[0])
                else:
                    if movimiento.startswith("(") and ")" in movimiento:
                        # Dos personas - encontrar todos los tiempos y tomar el máximo
                        import re
                        tiempos_encontrados = [int(x) for x in re.findall(r'\((\d+)\)', movimiento)]
                        tiempo = max(tiempos_encontrados) if tiempos_encontrados else 0
                    else:
                        tiempo = int(movimiento.split("(")[1].split(")")[0])
            except (ValueError, IndexError):
                tiempo = 0
        
        tiempo_acumulado += tiempo
        print(f"Paso {i}: {desc} → Tiempo: {tiempo} min (Total: {tiempo_acumulado} min)")
    
    print("=" * 50)
    print(f"TIEMPO TOTAL MÍNIMO: {tiempo_minimo} minutos")
    print("=" * 50)

# Pruebas
if __name__ == "__main__":
    casos = [
        ([1, 2], "CASO MUY SIMPLE"),
        ([1, 3, 4], "CASO 3 PERSONAS"), 
        ([1, 2, 5, 10], "CASO DE EJEMPLO")
    ]
    
    for tiempos, nombre in casos:
        print(f"\n{nombre}: {tiempos}")
        print(f"Resolviendo para tiempos: {tiempos}")
        print("Buscando solución óptima...\n")
        
        tiempo_min, solucion = resolver_puente(tiempos)
        mostrar_solucion(tiempos, tiempo_min, solucion)
        
        if nombre != casos[-1][1]:  # No imprimir separador después del último
            print("\n" + "="*70 + "\n")