import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data.csv")

plt.plot(data['value'])
plt.xlabel("Iteraciones")
plt.ylabel("Valor de la función")
plt.title("Simulated Annealing - Himmelblau")
plt.show()

plt.scatter(data['x'], data['y'], c=data['value'], cmap='viridis')
plt.plot(data['x'], data['y'], color='gray', alpha=0.5)
plt.colorbar(label='Valor de la función')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Recorrido del Simulated Annealing")
plt.show()
