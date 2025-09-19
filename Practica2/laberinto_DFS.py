import random
import time
from collections import deque

class LaberintoDFS:
    def __init__(self, filas=20, columnas=20):
        self.filas = filas
        self.columnas = columnas
        self.laberinto = []
        self.inicio = None
        self.salida = None
        self.camino = []
        
        # Definir constantes
        self.LIBRE = 0
        self.OBSTACULO = 1
        self.INICIO = 2
        self.SALIDA = 3
        self.CAMINO = 4
        self.VISITADO = 5
        
    def generar_laberinto(self, densidad_obstaculos=0.3):
        """Genera un laberinto aleatorio con obstÃ¡culos"""
        # Crear matriz llena de espacios libres
        self.laberinto = [[self.LIBRE for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Agregar obstÃ¡culos aleatorios
        for i in range(self.filas):
            for j in range(self.columnas):
                if random.random() < densidad_obstaculos:
                    self.laberinto[i][j] = self.OBSTACULO
        
        # Establecer punto de inicio (esquina superior izquierda)
        self.inicio = (0, 0)
        self.laberinto[0][0] = self.INICIO
        
        # Establecer salida (esquina inferior derecha)
        self.salida = (self.filas-1, self.columnas-1)
        self.laberinto[self.filas-1][self.columnas-1] = self.SALIDA
        
        # Asegurar que inicio y salida estÃ©n libres
        self.laberinto[0][0] = self.INICIO
        self.laberinto[self.filas-1][self.columnas-1] = self.SALIDA
        
        # Asegurar que haya al menos un camino posible
        self.asegurar_camino_posible()
        
        return self.laberinto
    
    def asegurar_camino_posible(self):
        """Asegura que exista al menos un camino desde inicio hasta salida"""
        # Crear un camino simple diagonal
        x, y = 0, 0
        while x < self.filas - 1 or y < self.columnas - 1:
            if random.random() < 0.5 and x < self.filas - 1:
                x += 1
            elif y < self.columnas - 1:
                y += 1
            self.laberinto[x][y] = self.LIBRE
        
        self.laberinto[self.filas-1][self.columnas-1] = self.SALIDA
    
    def es_valido(self, x, y):
        """Verifica si una posiciÃ³n es vÃ¡lida dentro del laberinto"""
        return 0 <= x < self.filas and 0 <= y < self.columnas
    
    def es_celda_libre(self, x, y):
        """Verifica si una celda estÃ¡ libre (no es obstÃ¡culo)"""
        if not self.es_valido(x, y):
            return False
        return (self.laberinto[x][y] == self.LIBRE or 
                self.laberinto[x][y] == self.SALIDA or
                self.laberinto[x][y] == self.INICIO)
    
    def dfs(self, x, y, visitados, camino_actual):
        """Algoritmo DFS para encontrar el camino"""
        # Si llegamos a la salida
        if (x, y) == self.salida:
            self.camino = camino_actual.copy()
            return True
        
        # Marcar como visitado
        visitados.add((x, y))
        
        # Movimientos posibles: arriba, derecha, abajo, izquierda
        movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(movimientos)  # Mezclar movimientos para exploraciÃ³n aleatoria
        
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            
            if (self.es_celda_libre(nx, ny) and (nx, ny) not in visitados):
                camino_actual.append((nx, ny))
                if self.dfs(nx, ny, visitados, camino_actual):
                    return True
                camino_actual.pop()  # Backtracking
        
        return False
    
    def resolver(self):
        """Resuelve el laberinto usando DFS"""
        visitados = set()
        camino_actual = [self.inicio]
        
        inicio_tiempo = time.time()
        encontrado = self.dfs(self.inicio[0], self.inicio[1], visitados, camino_actual)
        tiempo_ejecucion = time.time() - inicio_tiempo
        
        if encontrado:
            print(f"Â¡Camino encontrado! Longitud: {len(self.camino)} pasos")
            print(f"Tiempo de ejecuciÃ³n: {tiempo_ejecucion:.4f} segundos")
            return True
        else:
            print("No se encontrÃ³ camino posible")
            return False
    
    def mostrar_laberinto(self, mostrar_camino=False):
        """Muestra el laberinto en la consola con caracteres ASCII seguros"""
        # Usar caracteres ASCII bÃ¡sicos para evitar problemas de encoding
        simbolos = {
            self.LIBRE: '.',      # Punto para espacios libres
            self.OBSTACULO: '#',  # Numeral para obstÃ¡culos
            self.INICIO: 'I',     # S para inicio
            self.SALIDA: 'F',     # E para salida
            self.CAMINO: '*',     # Asterisco para el camino
            self.VISITADO: 'x'    # x para celdas visitadas
        }
        
        print("\n" + "+" + "-" * self.columnas + "+")
        
        for i in range(self.filas):
            print("|", end="")
            for j in range(self.columnas):
                if mostrar_camino and (i, j) in self.camino:
                    if (i, j) == self.inicio:
                        print('I', end="")
                    elif (i, j) == self.salida:
                        print('F', end="")
                    else:
                        print('*', end="")
                else:
                    celda = self.laberinto[i][j]
                    print(simbolos[celda], end="")
            print("|")
        
        print("+" + "-" * self.columnas + "+")
    
    def crear_laberinto_personalizado(self):
        """Crea un laberinto con un patrÃ³n especÃ­fico para testing"""
        self.laberinto = [[self.LIBRE for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Crear paredes exteriores
        for i in range(self.filas):
            for j in range(self.columnas):
                if i == 0 or i == self.filas-1 or j == 0 or j == self.columnas-1:
                    self.laberinto[i][j] = self.OBSTACULO
        
        # Crear algunos obstÃ¡culos internos
        for i in range(2, self.filas-2, 3):
            for j in range(2, self.columnas-2, 3):
                self.laberinto[i][j] = self.OBSTACULO
        
        # Establecer inicio y salida
        self.inicio = (1, 1)
        self.salida = (self.filas-2, self.columnas-2)
        self.laberinto[1][1] = self.INICIO
        self.laberinto[self.filas-2][self.columnas-2] = self.SALIDA
        
        # Crear un camino garantizado
        for i in range(1, self.filas-1):
            self.laberinto[i][self.columnas-3] = self.LIBRE
        for j in range(1, self.columnas-1):
            self.laberinto[self.filas-3][j] = self.LIBRE
        
        return self.laberinto

# FunciÃ³n principal
def main():
    # Crear y resolver laberinto
    laberinto = LaberintoDFS(20, 20)
    
    print("Generando laberinto...")
    laberinto.generar_laberinto(densidad_obstaculos=0.25)
    # laberinto.crear_laberinto_personalizado()
    
    print("Laberinto inicial:")
    laberinto.mostrar_laberinto()
    
    print("\nResolviendo con DFS...")
    if laberinto.resolver():
        print("\nLaberinto con soluciÃ³n:")
        laberinto.mostrar_laberinto(mostrar_camino=True)
        
        print(f"\nCoordenadas del camino ({len(laberinto.camino)} pasos):")
        for i, (x, y) in enumerate(laberinto.camino[:10]):  # Mostrar solo primeros 10 pasos
            print(f"Paso {i+1}: ({x}, {y})")
        if len(laberinto.camino) > 10:
            print(f"... y {len(laberinto.camino) - 10} pasos mÃ¡s")
    else:
        print("No se pudo encontrar una soluciÃ³n.")

if __name__ == "__main__":
    main()