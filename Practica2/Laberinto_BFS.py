import random
from collections import deque

class Laberinto:
    def __init__(self, n, m):
        self.tablero = [[-1 for _ in range(m)] for _ in range(n)]
        self.n = n
        self.m = m
        self.inicio = (random.randint(0, n - 1), random.randint(0, m - 1))
        self.final = (random.randint(0, n - 1), random.randint(0, m - 1))
        while self.inicio == self.final:
            self.final = (random.randint(0, n - 1), random.randint(0, m - 1))

# 1: Inicio, 2: Final, 0: Camino, 3: Muro, -1: Sin definir, 4: Camino solución

def generar_ruta(laberinto: Laberinto):
    x, y = laberinto.inicio
    xf, yf = laberinto.final
    laberinto.tablero[x][y] = 1
    while x != xf:
        x += 1 if x < xf else -1
        laberinto.tablero[x][y] = 0
    while y != yf:
        y += 1 if y < yf else -1
        laberinto.tablero[x][y] = 0
    laberinto.tablero[xf][yf] = 2

def generar_muros(laberinto: Laberinto, cantidad=10):
    n, m = laberinto.n, laberinto.m
    for _ in range(cantidad):
        x = random.randint(0, n - 1)
        y = random.randint(0, m - 1)
        if laberinto.tablero[x][y] == -1:
            laberinto.tablero[x][y] = 3

def generar_laberinto(n, m):
    lab = Laberinto(n, m)
    generar_ruta(lab)
    generar_muros(lab, cantidad=(n*m)//3)
    for i in range(lab.n):
        for j in range(lab.m):
            if lab.tablero[i][j] == -1:
                lab.tablero[i][j] = 0
    return lab

def es_movimiento_valido(laberinto: Laberinto, posicion):
    x, y = posicion
    if 0 <= x < laberinto.n and 0 <= y < laberinto.m:
        return laberinto.tablero[x][y] in [0, 2]
    return False

def resolver_bfs(laberinto: Laberinto):
    inicio = laberinto.inicio
    final = laberinto.final
    nodos_frontera = deque([inicio])
    nodos_visitados= []
    padres = {inicio: None}
    i=0

    while nodos_frontera:
        i+=1
        if i>4000:
            return None
        
        nodo_actual = nodos_frontera.popleft()

        if nodo_actual == final:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1] 
         
        nodos_visitados.append(nodo_actual)
        # Movimiento arriba
        if es_movimiento_valido(laberinto, (nodo_actual[0] + 1, nodo_actual[1])) and (nodo_actual[0] + 1, nodo_actual[1]) not in nodos_visitados and (nodo_actual[0] + 1, nodo_actual[1]) not in nodos_frontera:
            nodos_frontera.append((nodo_actual[0] + 1, nodo_actual[1]))
            padres[(nodo_actual[0] + 1, nodo_actual[1])] = nodo_actual
        # Movimiento abajo
        if es_movimiento_valido(laberinto, (nodo_actual[0] - 1, nodo_actual[1])) and (nodo_actual[0] - 1, nodo_actual[1]) not in nodos_visitados and (nodo_actual[0] - 1, nodo_actual[1]) not in nodos_frontera:
            nodos_frontera.append((nodo_actual[0] - 1, nodo_actual[1]))
            padres[(nodo_actual[0] - 1, nodo_actual[1])] = nodo_actual
        # Movimiento derecha
        if es_movimiento_valido(laberinto, (nodo_actual[0], nodo_actual[1] + 1)) and (nodo_actual[0], nodo_actual[1] + 1) not in nodos_visitados and (nodo_actual[0], nodo_actual[1] + 1) not in nodos_frontera:
            nodos_frontera.append((nodo_actual[0], nodo_actual[1] + 1))
            padres[(nodo_actual[0], nodo_actual[1] + 1)] = nodo_actual
        # Movimiento izquierda
        if es_movimiento_valido(laberinto, (nodo_actual[0], nodo_actual[1] - 1)) and (nodo_actual[0], nodo_actual[1] - 1) not in nodos_visitados and (nodo_actual[0], nodo_actual[1] - 1) not in nodos_frontera:
            nodos_frontera.append((nodo_actual[0], nodo_actual[1] - 1))
            padres[(nodo_actual[0], nodo_actual[1] - 1)] = nodo_actual

def mostrar_laberinto_con_camino(laberinto, camino):
    # Crear una copia del tablero
    visualizacion = [fila[:] for fila in laberinto.tablero]
    
    # Marcar el camino (excepto inicio y final)
    for pos in camino[1:-1]:  # Excluir inicio (1) y final (2)
        x, y = pos
        visualizacion[x][y] = 4  # Usar 4 para representar el camino
    
    print("Laberinto con camino solución:")
    for fila in visualizacion:
        print(' '.join(str(celda).rjust(2) for celda in fila))


n = 10
m = 10
lab = generar_laberinto(n, m)
for i in range(n):
    print(f" {i} ", end="")
print()
j=0
for fila in lab.tablero:
    print(f"{fila} {j}")
    j+=1

print("Resolviendo laberinto...")
camino = resolver_bfs(lab)

if camino:
    print("Laberinto resuelto!")
    print(f"Camino encontrado ({len(camino)} pasos):")
    for paso, posicion in enumerate(camino):
        print(f"Paso {paso}: {posicion}")
    mostrar_laberinto_con_camino(lab, camino)
else:
    print("No se pudo resolver el laberinto.")