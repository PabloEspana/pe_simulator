# Con esto se podrá graficar en python
# Ejemplos

from scipy.stats import poisson, binom
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


"""data = [19, 16, 18, 15, 18, 18, 24, 24, 22, 20]
data2 = [ 2, 3, 3, 4, 3, 3, 3, 3, 3, 3]
plt.hist(data2, color = "c", ec="skyblue")
plt.title('Histograma de frecuencias')
plt.ylabel('Frecuencia')
plt.xlabel('Número de clientes')
plt.grid(True)
plt.show()"""


# grafica llegadas de clientes
"""x = ['14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
y = [19, 16, 18, 15, 18, 18, 24, 24, 22, 20]
plt.plot(x, y, color="r")
plt.title('Llegadas de clientes')
plt.ylabel('Cantidad de clientes')
plt.xlabel('Hora')
#plt.grid(True)
plt.show()"""

# grafica tiempos de servicio en una hora
"""x = ['14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
y = [2, 3, 3, 4, 3, 3, 3, 3, 3, 3]
plt.plot(x, y, color="y")
plt.title('Tiempo de servicio de clientes')
plt.ylabel('Tiempo de servicio (min)')
plt.xlabel('Hora')
#plt.grid(True)
plt.show()"""



#Simulacion

# grafica tiempos entre llegada en 20 eventos
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [0.66, 1.14, 0.78, 8.34, 1.8, 4.32, 6.18, 4.62, 2.04, 14.52, 1.08, 1.62, 1.2, 0.06, 2.4, 5.94, 10.14, 6.42, 2.7, 0.24]
plt.plot(x, y, color="r")
plt.title('Tiempo entre llegadas de clientes en la simulación')
plt.ylabel('Tiempo entre llegada (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""


# grafica tiempos de servicio en 20 eventos
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [1.5, 2.1, 1.62, 0.36, 3.06, 8.94, 0.18, 0.5, 3.36, 0.6, 2.04, 2.82, 2.16, 0.78, 4.02, 0.12, 0.48, 0.18, 4.5, 1.02]
plt.plot(x, y, color="b")
plt.title('Tiempo de servicio de clientes en la simulación')
plt.ylabel('Tiempo de servicio (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""


# grafica tiempos de espera un solo canal
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [0, 0.36, 1.74, 0, 0, 0, 2.76, 0, 8.46, 0, 0, 0.42, 2.04, 4.14, 2.46, 0.54, 0, 0, 0, 4.26]
plt.plot(x, y, color="r")
plt.title('Tiempo de espera de clientes en simulación de un solo canal')
plt.ylabel('Tiempo de espera (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""

# grafica tiempos de espera de dos canales
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.56, 0, 0, 0, 0, 0, 0]
plt.plot(x, y, color="g")
plt.title('Tiempo de espera de clientes en simulación de dos canales')
plt.ylabel('Tiempo de espera (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""


# grafica tiempos en el sistema de un canal
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [1.5, 2.46, 3.3, 0.36, 3.06, 8.94, 2.94, 10.5, 11.82, 0.6, 2.04, 3.18, 4.2, 4.86, 6.48, 0.66, 0.48, 0.18, 4.5, 5.22]
plt.plot(x, y, color="r")
plt.title('Tiempo en el sistema en simulación de un canal')
plt.ylabel('Tiempo de espera (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""


# grafica tiempos en el sistema de dos canales
"""x = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
y = [1.5, 2.1, 1.62, 0.36, 3.06, 8.94, 0.18, 10.5, 3.36, 0.6, 2.04, 2.82, 2.16, 2.28, 4.02, 0.12, 0.48, 0.18, 4.5, 1.02]
plt.plot(x, y, color="g")
plt.title('Tiempo en el sistema en simulación de dos canales')
plt.ylabel('Tiempo de espera (min)')
plt.xlabel('Número de cliente')
#plt.grid(True)
plt.show()"""

# grafica final de tiempos de servicios



"""x = [1.36, 0.08]
y = ["1 Canal", "2 Canales"]
#plt.axes((0.1, 0.3, 0.8, 0.6))  # Definimos la posición de los ejes
plt.bar(np.arange(2), x, color="y")  # Dibujamos el gráfico de barras
#plt.ylim(550,650)  # Limitamos los valores del eje y al range definido [450, 550]
plt.title('Comparación de tiempos de espera en simulación de \n linea de espera de un canal y dos canales')  # Colocamos el título
plt.xticks(np.arange(2), y) 
plt.show()
"""


 


x = np.array([1,2,3,4, 5, 6, 7])
y = np.array([700,750,750,840,780,780,850] )
gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
mn=np.min(x)
mx=np.max(x)
x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept
plt.plot(x,y,'ob') # puntos
plt.plot(x1,y1,'-r') # linea
plt.title('Llegadas de clientes en las ultimas semanas')
plt.ylabel('Cantidad de clientes')
plt.xlabel('Semana')
#plt.grid(True)
plt.show()