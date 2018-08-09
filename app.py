import sys, os, datetime
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import math
import operator
import qdarkstyle

from scipy.stats import poisson, binom
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


ventanPrincipal, QtBaseClass = uic.loadUiType('aleatorios.ui')
Ui_MainWindow_Aleatorios, QtBaseClass2 = uic.loadUiType('n_aleatorios.ui')
Ui_MainWindow_Simulacion, QtBaseClass3 = uic.loadUiType('simulacion.ui')
Ui_MainWindow_SimulacionLinea, QtBaseClass4 = uic.loadUiType('simulacion_linea.ui')
Ui_MainWindow_SimulacionLinea2, QtBaseClass5 = uic.loadUiType('simulacion_linea2.ui')
Ui_MainWindow_Regresion, QtBaseClass6 = uic.loadUiType('regresion_lineal.ui')


datos = []
suma = 0
r_menor  = 0
r_mayor = 0
datos2 = []
suma2 = 0
r_menor2  = 0
r_mayor2 = 0
n_aleatorios = []
n_aleatorios_llegada = []
n_aleatorios_servicio = []
tasa_de_llegada = 0
tasa_de_servicio = 0
promedio_llegada = 0
promedio_servicio = 0
suma_frecuencias_clientes = 0
suma_frecuencias_tiempos = 0

datos_regresionX = []
datos_regresionY = []


class ventanaRegresion(QtWidgets.QMainWindow, Ui_MainWindow_Regresion):
	def __init__(self, parent=None):
		super(ventanaRegresion, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow_Regresion.__init__(self)
		self.setupUi(self)
		self.btnAgregarDatos.clicked.connect(self.agregarDatos)
		self.btnPredecir.clicked.connect(self.predecir)
		#Validaciones
		self.txtSemana.setValidator(QtGui.QIntValidator())
		self.txtCantidad.setValidator(QtGui.QIntValidator())
		self.txtValor.setValidator(QtGui.QIntValidator())

	def agregarDatos(self):
		if (len(self.txtSemana.text())==0 or len(self.txtCantidad.text())==0 
		or int(self.txtSemana.text())<=0 or int(self.txtCantidad.text())<=0 ):
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			semama = int(self.txtSemana.text())
			cantidad = int(self.txtCantidad.text())
			datos_regresionX.append(semama)
			datos_regresionY.append(cantidad)
			self.tabla_datos.setRowCount(len(datos_regresionX))
			for i in range(len(datos_regresionX)):
				self.tabla_datos.setItem(i, 0, QtWidgets.QTableWidgetItem(str( datos_regresionX[i] ) ))
				self.tabla_datos.setItem(i, 1, QtWidgets.QTableWidgetItem(str( datos_regresionY[i] ) ))


		x = np.array(datos_regresionX)
		y = np.array(datos_regresionY)
		gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
		mn=np.min(x)
		mx=np.max(x)
		x1=np.linspace(mn,mx,500)
		y1=gradient*x1+intercept
		plt.plot(x,y,'ob') # puntos
		plt.plot(x1,y1,'-r') # linea
		plt.title('Regresión Lineal')
		plt.ylabel('Valores en Y')
		plt.xlabel('Valores en X')
		plt.savefig('./imagenes/regresion.png', dpi=100)
		plt.close()

		self.grafico.setPixmap(QtGui.QPixmap(os.getcwd() + "/imagenes/regresion.png"))
		self.grafico.setScaledContents(True)

	def predecir(self):
		if len(datos_regresionX) == 0:
			QtWidgets.QMessageBox.information(self, "Error", "Ingrese primero valores en X y Y", QtWidgets.QMessageBox.Ok)
		else:
			if len(self.txtValor.text()) == 0 or int(self.txtValor.text())<=0:
				QtWidgets.QMessageBox.information(self, "Error", "Ingrese el valor a predecir", QtWidgets.QMessageBox.Ok)
			else:
				valor = int(self.txtValor.text())
				sumatoriaX = np.sum(datos_regresionX)
				sumatoriaY = np.sum(datos_regresionY)
				XY = list(map(operator.mul, datos_regresionX, datos_regresionY))
				X2 = list(map(operator.mul, datos_regresionX, datos_regresionX))
				sumatoriaXY =  np.sum(XY)
				sumatoriaX2 =  np.sum(X2)
				a0 = ((sumatoriaY * sumatoriaX2) - (sumatoriaX * sumatoriaXY)) / ((len(datos_regresionX) * sumatoriaX2 ) - (sumatoriaX**2))
				a1 = ((len(datos_regresionX) * sumatoriaXY ) - (sumatoriaX * sumatoriaY)) / ((len(datos_regresionX) * sumatoriaX2 ) - (sumatoriaX**2))
				newY = a0 + (a1*valor)
				self.resultado.setText("Valor predecido: "+str("{0:.0f}".format(newY)))


class ventanaSimulacionLineaEspera2(QtWidgets.QMainWindow, Ui_MainWindow_SimulacionLinea2):
	def __init__(self, parent=None):
		super(ventanaSimulacionLineaEspera2, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow_SimulacionLinea2.__init__(self)
		self.setupUi(self)
		self.btnLineaEspera.clicked.connect(self.linea_Espera)
		self.btnObtenerValores.clicked.connect(self.obtenerValores)
		#Validaciones
		self.txtLanda.setValidator(QtGui.QIntValidator())
		self.txtNiu.setValidator(QtGui.QIntValidator())
		self.txtEventosLinea.setValidator(QtGui.QIntValidator())
		
	def obtenerValores(self):
		self.txtLanda.setText(str(int(promedio_llegada)))
		if promedio_servicio > 0:
			self.txtNiu.setText(str(int(60 / promedio_servicio)))
		else:
			self.txtNiu.setText(str(0))

	def linea_Espera(self):
		if (len(self.txtLanda.text())==0 or len(self.txtNiu.text())==0 or len(self.txtEventosLinea.text())==0 
		or int(self.txtLanda.text())<=0 or int(self.txtNiu.text())<=0 or int(self.txtEventosLinea.text())<=0 ):
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			landa = int(self.txtLanda.text())
			niu = int(self.txtNiu.text())
			numero_eventos_linea = int(self.txtEventosLinea.text())
			hora_llegada = 0
			hora_inicializacion_servicio1 = 0
			hora_terminacion_servicio1= 0
			hora_inicializacion_servicio2 = 0
			hora_terminacion_servicio2 = 0
			tiempo_de_espera = 0
			total1 = 0
			total2 = 0 
			total3 = 0 
			total4 = 0
			promedio1 = 0 
			promedio2 = 0
			promedio3 = 0 
			promedio4 = 0
			canal_usado = 1
			hora_iniciacion_servicio_anterior1 = 0
			hora_terminacion_servicio_anterior1 = 0
			hora_iniciacion_servicio_anterior2 = 0
			hora_terminacion_servicio_anterior2 = 0
			self.tabla_linea_espera.setRowCount(numero_eventos_linea)
			for i in range(numero_eventos_linea):

				#Canal usado
				if hora_terminacion_servicio_anterior1 <= hora_terminacion_servicio_anterior2:
					canal_usado = 1
					hora_inicializacion_servicio2 = hora_iniciacion_servicio_anterior2
					hora_terminacion_servicio2 = hora_terminacion_servicio_anterior2
				else:
					canal_usado = 2
					hora_inicializacion_servicio1 = hora_iniciacion_servicio_anterior1
					hora_terminacion_servicio1 = hora_terminacion_servicio_anterior1

				tiempo_entre_llegadas = (-1/landa)*(math.log(n_aleatorios_llegada[i]))
				tiempo_de_servicios = (-1/niu)*(math.log(n_aleatorios_servicio[i]))
				hora_llegada = hora_llegada + tiempo_entre_llegadas

				self.tabla_linea_espera.setItem(i, 0, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(n_aleatorios_llegada[i]) ) ))
				self.tabla_linea_espera.setItem(i, 1, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(n_aleatorios_servicio[i]) ) ))
				self.tabla_linea_espera.setItem(i, 2, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_entre_llegadas)  ) ))
				self.tabla_linea_espera.setItem(i, 3, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_de_servicios) ) ))
				self.tabla_linea_espera.setItem(i, 4, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_llegada) ) ))
				self.tabla_linea_espera.setItem(i, 5, QtWidgets.QTableWidgetItem(str(  canal_usado ) ))
				
				if canal_usado == 1:
					if hora_llegada > hora_terminacion_servicio1:
						hora_inicializacion_servicio1 = hora_llegada
					else:
						hora_inicializacion_servicio1 = hora_terminacion_servicio1
				if canal_usado == 2:
					if hora_llegada > hora_terminacion_servicio2:
						hora_inicializacion_servicio2 = hora_llegada
					else:
						hora_inicializacion_servicio2 = hora_terminacion_servicio2
				
				if canal_usado == 1:
					self.tabla_linea_espera.setItem(i, 6, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_inicializacion_servicio1) ) ))
					hora_terminacion_servicio1 = hora_inicializacion_servicio1 + tiempo_de_servicios
					self.tabla_linea_espera.setItem(i, 7, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_terminacion_servicio1) ) ))         
				if canal_usado == 2:
					self.tabla_linea_espera.setItem(i, 8, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_inicializacion_servicio2) ) ))
					hora_terminacion_servicio2 = hora_inicializacion_servicio2 + tiempo_de_servicios
					self.tabla_linea_espera.setItem(i, 9, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_terminacion_servicio2) ) ))         

				if canal_usado == 1:
					tiempo_de_espera = hora_inicializacion_servicio1 - hora_llegada
				if canal_usado == 2:
					tiempo_de_espera = hora_inicializacion_servicio2 - hora_llegada

				self.tabla_linea_espera.setItem(i, 10, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_de_espera) ) ))      
				tiempo_sistema = tiempo_de_espera + tiempo_de_servicios
				self.tabla_linea_espera.setItem(i, 11, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_sistema) ) ))
				
				hora_terminacion_servicio_anterior1 = hora_terminacion_servicio1
				hora_iniciacion_servicio_anterior1 = hora_inicializacion_servicio1
				hora_terminacion_servicio_anterior2 = hora_terminacion_servicio2
				hora_iniciacion_servicio_anterior2 = hora_inicializacion_servicio2

				
				
				
				total1 += tiempo_entre_llegadas
				promedio1 = float(total1 / numero_eventos_linea)
				self.totalTiempoEntreLlegada.setText(str("{0:.2f}".format(total1 * 60)))
				self.promedioTiempoEntreLlegada.setText(str("{0:.2f}".format(promedio1 * 60)))

				total2 += tiempo_de_servicios
				promedio2 = float(total2 / numero_eventos_linea)
				self.totalTiempoServicio.setText(str("{0:.2f}".format(total2 * 60)))
				self.promedioTiempoServicio.setText(str("{0:.2f}".format(promedio2 * 60)))

				total3 += tiempo_sistema
				promedio3 = float(total3 / numero_eventos_linea)
				self.totalTiempoSistema.setText(str("{0:.2f}".format(total3 * 60)))
				self.promedioTiempoSistema.setText(str("{0:.2f}".format(promedio3 * 60)))

				total4 += tiempo_de_espera
				promedio4 = float(total4 / numero_eventos_linea)
				self.totalTiempoEspera.setText(str("{0:.2f}".format(total4 * 60)))
				self.promedioTiempoEspera.setText(str("{0:.2f}".format(promedio4 * 60)))




class ventanaSimulacionLineaEspera(QtWidgets.QMainWindow, Ui_MainWindow_SimulacionLinea):
	def __init__(self, parent=None):
		super(ventanaSimulacionLineaEspera, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow_SimulacionLinea.__init__(self)
		self.setupUi(self)
		self.btnLineaEspera.clicked.connect(self.linea_Espera)
		self.btnObtenerValores.clicked.connect(self.obtenerValores)
		# Validaciones
		self.txtLanda.setValidator(QtGui.QIntValidator())
		self.txtNiu.setValidator(QtGui.QIntValidator())
		self.txtEventosLinea.setValidator(QtGui.QIntValidator())
		
	def obtenerValores(self):
		self.txtLanda.setText(str(int(promedio_llegada)))
		if promedio_servicio > 0:
			self.txtNiu.setText(str(int(60 / promedio_servicio)))
		else:
			self.txtNiu.setText(str(0))

	def linea_Espera(self):
		if (len(self.txtLanda.text())==0 or len(self.txtNiu.text())==0 or len(self.txtEventosLinea.text())==0 
		or int(self.txtLanda.text())<=0 or int(self.txtNiu.text())<=0 or int(self.txtEventosLinea.text())<=0 ):
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			landa = int(self.txtLanda.text())
			niu = int(self.txtNiu.text())
			numero_eventos_linea = int(self.txtEventosLinea.text())
			hora_llegada = 0
			hora_inicializacion_servicio = 0
			hora_terminacion_servicio = 0
			tiempo_de_espera = 0
			hora_terminacion_servicio_anterior = 0
			total1 = 0
			total2 = 0 
			total3 = 0 
			total4 = 0
			promedio1 = 0 
			promedio2 = 0
			promedio3 = 0 
			promedio4 = 0
			self.tabla_linea_espera.setRowCount(numero_eventos_linea)
			for i in range(numero_eventos_linea):
				tiempo_entre_llegadas = (-1/landa)*(math.log(n_aleatorios_llegada[i]))
				tiempo_de_servicios = (-1/niu)*(math.log(n_aleatorios_servicio[i]))
				hora_llegada = hora_llegada + tiempo_entre_llegadas
				self.tabla_linea_espera.setItem(i, 0, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(n_aleatorios_llegada[i]) ) ))
				self.tabla_linea_espera.setItem(i, 1, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(n_aleatorios_servicio[i]) ) ))
				self.tabla_linea_espera.setItem(i, 2, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_entre_llegadas)  ) ))
				self.tabla_linea_espera.setItem(i, 3, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_de_servicios) ) ))
				self.tabla_linea_espera.setItem(i, 4, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_llegada) ) ))
				if hora_llegada > hora_terminacion_servicio:
					hora_inicializacion_servicio = hora_llegada
				else:
					hora_inicializacion_servicio = hora_terminacion_servicio
				self.tabla_linea_espera.setItem(i, 5, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_inicializacion_servicio) ) ))
				hora_terminacion_servicio = hora_inicializacion_servicio + tiempo_de_servicios
				self.tabla_linea_espera.setItem(i, 6, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(hora_terminacion_servicio) ) ))         
				if hora_terminacion_servicio_anterior - hora_llegada > 0:
					tiempo_de_espera = hora_terminacion_servicio_anterior - hora_llegada
				else:
					tiempo_de_espera = 0
				self.tabla_linea_espera.setItem(i, 7, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_de_espera) ) ))      
				tiempo_sistema = tiempo_de_espera + tiempo_de_servicios
				self.tabla_linea_espera.setItem(i, 8, QtWidgets.QTableWidgetItem(str(  "{0:.3f}".format(tiempo_sistema) ) ))
				hora_terminacion_servicio_anterior = hora_terminacion_servicio

				total1 += tiempo_entre_llegadas
				promedio1 = float(total1 / numero_eventos_linea)
				self.totalTiempoEntreLlegada.setText(str("{0:.2f}".format(total1 * 60)))
				self.promedioTiempoEntreLlegada.setText(str("{0:.2f}".format(promedio1 * 60)))

				total2 += tiempo_de_servicios
				promedio2 = float(total2 / numero_eventos_linea)
				self.totalTiempoServicio.setText(str("{0:.2f}".format(total2 * 60)))
				self.promedioTiempoServicio.setText(str("{0:.2f}".format(promedio2 * 60)))

				total3 += tiempo_sistema
				promedio3 = float(total3 / numero_eventos_linea)
				self.totalTiempoSistema.setText(str("{0:.2f}".format(total3 * 60)))
				self.promedioTiempoSistema.setText(str("{0:.2f}".format(promedio3 * 60)))

				total4 += tiempo_de_espera
				promedio4 = float(total4 / numero_eventos_linea)
				self.totalTiempoEspera.setText(str("{0:.2f}".format(total4 * 60)))
				self.promedioTiempoEspera.setText(str("{0:.2f}".format(promedio4 * 60)))


class ventanaSimulacion(QtWidgets.QMainWindow, Ui_MainWindow_Simulacion):
	def __init__(self, parent=None):
		super(ventanaSimulacion, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow_Simulacion.__init__(self)
		self.setupUi(self)
		self.btnAgregarDemanda.clicked.connect(self.agregar_Demanda)
		self.btnAgregarTiempo.clicked.connect(self.agregar_Tiempo)
		self.btnSimular.clicked.connect(self.simulacion)
		self.btnSimularTiempos.clicked.connect(self.simulacionTiempo)
		self.tabla_funcion.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.tabla_funcion.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.tabla_funcion.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

		# Validaciones
		self.txtCantidadCliente.setValidator(QtGui.QIntValidator())
		self.txtFrecuenciaCantidad.setValidator(QtGui.QIntValidator())
		self.txtTiempoServicio.setValidator(QtGui.QIntValidator())
		self.txtFrecuenciaTiempo.setValidator(QtGui.QIntValidator())
		self.txtEventos.setValidator(QtGui.QIntValidator())
		self.txtEventos_2.setValidator(QtGui.QIntValidator())

	def agregar_Demanda(self):
		global datos, suma, r_menor, r_mayor, tasa_de_llegada, suma_frecuencias_clientes, promedio_llegada
		suma = 0
		r_menor=0
		r_mayor=0
		suma_dias = 0
		if len(self.txtCantidadCliente.text())==0 or len(self.txtFrecuenciaCantidad.text())==0:
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			cantidad = int(self.txtCantidadCliente.text())
			frecuencia = int(self.txtFrecuenciaCantidad.text())
			datos.append([cantidad, frecuencia, 0, 0, 0, 0])
			for i in range(len(datos)): # Sumatoria de dias
				suma_dias += datos[i][1]
			for i in range(len(datos)): # probabilidad
				datos[i][2] = (datos[i][1] / suma_dias)
			for i in range(len(datos)): # probabilidad acumulada
				datos[i][3] = datos[i][2] + suma
				suma = datos[i][3]
			for i in range(len(datos)): # rangos
				datos[i][4] = r_menor
				datos[i][5] = (datos[i][3])
				r_menor = datos[i][5] + 0.001
			
			suma_frecuencias_clientes += frecuencia
			tasa_de_llegada += cantidad * frecuencia
			promedio_llegada = tasa_de_llegada / suma_frecuencias_clientes
			promedio_llegada = round(promedio_llegada, 0)

			self.tabla_funcion.setRowCount(len(datos)) # Numero de filas
			for i in range(len(datos)): # Completar tabla demanda-dias
				self.tabla_funcion.setItem(i, 0, QtWidgets.QTableWidgetItem(str( datos[i][0] ) ))
				self.tabla_funcion.setItem(i, 1, QtWidgets.QTableWidgetItem(str( datos[i][1] ) ))
				btn = QtWidgets.QPushButton(self.tabla_funcion)
				btn.setText('X')
				btn.setStyleSheet("background-color: #E57373; width: 150px;")
				self.tabla_funcion.setCellWidget(i, 2, btn)
			

			self.tabla_completa.setRowCount(len(datos))
			for i in range(len(datos)): # Completar tabla de probabilidades
				self.tabla_completa.setItem(i, 0, QtWidgets.QTableWidgetItem(str( datos[i][0] ) ))
				self.tabla_completa.setItem(i, 1, QtWidgets.QTableWidgetItem(str( "{0:.2f}".format(datos[i][2]) ) ))
				self.tabla_completa.setItem(i, 2, QtWidgets.QTableWidgetItem(str( "{0:.2f}".format(datos[i][3]) ) ))
				self.tabla_completa.setItem(i, 3, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(datos[i][4]) ) ))
				self.tabla_completa.setItem(i, 4, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(datos[i][5]) ) ))

	def agregar_Tiempo(self):
		global datos2, suma2, r_menor2, r_mayor2, tasa_de_servicio, suma_frecuencias_tiempos, promedio_servicio
		suma2 = 0
		r_menor2=0
		r_mayor2=0
		suma_dias2 = 0
		if len(self.txtTiempoServicio.text())==0 or len(self.txtFrecuenciaTiempo.text())==0:
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			tiempo = int(self.txtTiempoServicio.text())
			frecuencia_tiempo = int(self.txtFrecuenciaTiempo.text())
			datos2.append([tiempo, frecuencia_tiempo, 0, 0, 0, 0])
			for i in range(len(datos2)): # Sumatoria de dias
				suma_dias2 += datos2[i][1]
			for i in range(len(datos2)): # probabilidad
				datos2[i][2] = (datos2[i][1] / suma_dias2)
			for i in range(len(datos2)): # probabilidad acumulada
				datos2[i][3] = datos2[i][2] + suma2
				suma2 = datos2[i][3]
			for i in range(len(datos2)): # rangos
				datos2[i][4] = r_menor2
				datos2[i][5] = (datos2[i][3])
				r_menor2 = datos2[i][5] + 0.001

			suma_frecuencias_tiempos += frecuencia_tiempo
			tasa_de_servicio += tiempo * frecuencia_tiempo
			promedio_servicio = tasa_de_servicio / suma_frecuencias_tiempos
			promedio_servicio = round(promedio_servicio, 0)

			self.tabla_funcion_tiempo.setRowCount(len(datos2)) # Numero de filas
			for i in range(len(datos2)): # Completar tabla demanda-dias
				self.tabla_funcion_tiempo.setItem(i, 0, QtWidgets.QTableWidgetItem(str( datos2[i][0] ) ))
				self.tabla_funcion_tiempo.setItem(i, 1, QtWidgets.QTableWidgetItem(str( datos2[i][1] ) ))

			self.tabla_completa_tiempo.setRowCount(len(datos2))
			for i in range(len(datos2)): # Completar tabla de probabilidades
				self.tabla_completa_tiempo.setItem(i, 0, QtWidgets.QTableWidgetItem(str( datos2[i][0] ) ))
				self.tabla_completa_tiempo.setItem(i, 1, QtWidgets.QTableWidgetItem(str( "{0:.2f}".format(datos2[i][2]) ) ))
				self.tabla_completa_tiempo.setItem(i, 2, QtWidgets.QTableWidgetItem(str( "{0:.2f}".format(datos2[i][3]) ) ))
				self.tabla_completa_tiempo.setItem(i, 3, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(datos2[i][4]) ) ))
				self.tabla_completa_tiempo.setItem(i, 4, QtWidgets.QTableWidgetItem(str( "{0:.3f}".format(datos2[i][5]) ) ))


	def simulacion(self):
		totalLlegada = 0
		promedioLlegada = 0
		if len(self.txtEventos.text())==0 or int(self.txtEventos.text())<=0:
			QtWidgets.QMessageBox.information(self, "Error", "Ingrese la cantidad de eventos", QtWidgets.QMessageBox.Ok)
		else:
			numero_eventos = int(self.txtEventos.text())
			self.tabla_simulacion.setRowCount(numero_eventos)
			for i in range(numero_eventos):
				for j in range(len(datos)):
					if n_aleatorios_llegada[i] >= datos[j][4] and n_aleatorios_llegada[i] <= datos[j][5]:
						self.tabla_simulacion.setItem(i, 0, QtWidgets.QTableWidgetItem( str(  "{0:.3f}".format(n_aleatorios_llegada[i]) )))
						self.tabla_simulacion.setItem(i, 1, QtWidgets.QTableWidgetItem( str(datos[j][0]) ))
						totalLlegada += datos[j][0]
						break
			promedioLlegada = float(totalLlegada / numero_eventos)
			self.lblTotalLlegadas.setText("Total : " + str(totalLlegada))
			self.lblPromedioLlegadas.setText("Promedio : " + str("{0:.2f}".format(promedioLlegada)))

	def simulacionTiempo(self):
		totalServicio = 0
		promedioServicio = 0
		if len(self.txtEventos_2.text())==0 or int(self.txtEventos_2.text())<=0:
			QtWidgets.QMessageBox.information(self, "Error", "Ingrese la cantidad de eventos", QtWidgets.QMessageBox.Ok)
		else:
			numero_eventos2 = int(self.txtEventos_2.text())
			self.tabla_simulacion_2.setRowCount(numero_eventos2)
			for i in range(numero_eventos2):
				for j in range(len(datos2)):
					if n_aleatorios_servicio[i] >= datos2[j][4] and n_aleatorios_servicio[i] <= datos2[j][5]:
						self.tabla_simulacion_2.setItem(i, 0, QtWidgets.QTableWidgetItem( str(  "{0:.3f}".format(n_aleatorios_servicio[i]) )))
						self.tabla_simulacion_2.setItem(i, 1, QtWidgets.QTableWidgetItem( str(datos2[j][0]) ))
						totalServicio += datos2[j][0]
						break
			promedioServicio = float(totalServicio / numero_eventos2)
			self.lblTotalServicio.setText("Total : " + str(totalServicio))
			self.lblPromedioServicio.setText("Promedio : " + str("{0:.2f}".format(promedioServicio)))


class ventanaAleatorios(QtWidgets.QMainWindow, Ui_MainWindow_Aleatorios):
	def __init__(self, parent=None):
		super(ventanaAleatorios, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow_Aleatorios.__init__(self)
		self.setupUi(self)
		self.tabla.clear()
		self.tabla.setColumnCount(4)
		self.tabla.setHorizontalHeaderLabels(['Xn', 'aXn+c', '(aXn+c)mod m', 'ri'])
		self.tabla.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.tabla.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.tabla.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		self.tabla.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
		self.tabla_2.clear()
		self.tabla_2.setColumnCount(4)
		self.tabla_2.setHorizontalHeaderLabels(['Xn', 'aXn+c', '(aXn+c)mod m', 'ri'])
		self.tabla_2.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.tabla_2.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.tabla_2.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		self.tabla_2.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

		self.btnGenerar.clicked.connect(self.generar_Aleatorios)

		# Validaciones
		self.txtA.setValidator(QtGui.QIntValidator())
		self.txtC.setValidator(QtGui.QIntValidator())
		self.txtXn.setValidator(QtGui.QIntValidator())
		self.txtM.setValidator(QtGui.QIntValidator())
		self.txtCantidad.setValidator(QtGui.QIntValidator())

	
	def generar_Aleatorios(self):
		global n_aleatorios_llegada
		global n_aleatorios_servicio
		if len(self.txtA.text())==0 or len(self.txtC.text())==0 or len(self.txtXn.text())==0 or len(self.txtM.text())==0 or len(self.txtCantidad.text())==0:
			QtWidgets.QMessageBox.information(self, "Error", "Complete todos los campos", QtWidgets.QMessageBox.Ok)
		else:
			cantidad = int(self.txtCantidad.text())
			total = cantidad * 2
			self.tabla.setRowCount(cantidad)
			self.tabla_2.setRowCount(cantidad)
			a = int(self.txtA.text())
			c = int(self.txtC.text())
			Xn =  int(self.txtXn.text())
			m = int(self.txtM.text())
			n_aleatorios_llegada = []
			n_aleatorios_servicio = []

			for i in range(cantidad):
				self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str( Xn ) ))
				self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(str( (a * Xn) + c) ))
				self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str( ((a * Xn) + c) % m) ))
				n_aleatorios_llegada.append( (((a * Xn) + c) % m) / (m -1) )
				self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(str("{0:.3f}".format( (((a * Xn) + c) % m) / (m -1) )) ))
				Xn = ((a * Xn) + c) % m

			for i in range(cantidad):
				self.tabla_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str( Xn ) ))
				self.tabla_2.setItem(i, 1, QtWidgets.QTableWidgetItem(str( (a * Xn) + c) ))
				self.tabla_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str( ((a * Xn) + c) % m) ))
				n_aleatorios_servicio.append( (((a * Xn) + c) % m) / (m -1) )
				self.tabla_2.setItem(i, 3, QtWidgets.QTableWidgetItem(str("{0:.3f}".format( (((a * Xn) + c) % m) / (m -1) )) ))
				Xn = ((a * Xn) + c) % m

			x = np.arange(0, len(n_aleatorios_llegada))
			y = n_aleatorios_llegada
			plt.plot(x, y)
			plt.title('Aleatorios de llegada')
			plt.ylabel('Valor')
			plt.xlabel('Número de aleatorio')
			plt.grid(True)
			plt.savefig('./imagenes/a_llegada.png', dpi=100)
			plt.close()

			x2 = np.arange(0, len(n_aleatorios_servicio))
			y2 = n_aleatorios_servicio
			plt.plot(x2, y2)
			plt.title('Aleatorios de servicio')
			plt.ylabel('Valor')
			plt.xlabel('Número de aleatorio')
			plt.grid(True)
			plt.savefig('./imagenes/a_servicio.png', dpi=100)
			plt.close()

			self.grafico_llegada.setPixmap(QtGui.QPixmap(os.getcwd() + "/imagenes/a_llegada.png"))
			self.grafico_llegada.setScaledContents(True)
			self.grafico_servicio.setPixmap(QtGui.QPixmap(os.getcwd() + "/imagenes/a_servicio.png"))
			self.grafico_servicio.setScaledContents(True)


		


class Aleatorios(QtWidgets.QMainWindow, ventanPrincipal):
	
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		ventanPrincipal.__init__(self)
		self.setupUi(self)
		self.showMaximized()
		self.enlace_github.clicked.connect(self.abrir_github)
		
		self.ventana2 = ventanaAleatorios(self)
		self.ventana3 = ventanaSimulacion(self)
		self.ventana4 = ventanaSimulacionLineaEspera(self)
		self.ventana5 = ventanaSimulacionLineaEspera2(self)
		self.ventana6 = ventanaRegresion(self)

		menu = self.menuBar()
		menu_aleatorios = menu.addMenu("&Menú")
  
		menu_aleatorios_abrir = QtWidgets.QAction(QtGui.QIcon(), "&Números aleatorios", self)
		menu_aleatorios_abrir.setShortcut("Ctrl+a") #Atajo de teclado
		menu_aleatorios_abrir.setStatusTip("Aleatorios") #Mensaje en la barra de estado
		menu_aleatorios_abrir.triggered.connect(self.menuAbrirAleatorios) #Lanzador
		menu_aleatorios.addAction(menu_aleatorios_abrir)

		menu_simulacion_abrir = QtWidgets.QAction(QtGui.QIcon(), "&Montecarlo", self)
		menu_simulacion_abrir.setShortcut("Ctrl+m") #Atajo de teclado
		menu_simulacion_abrir.setStatusTip("Simulación montecarlo") #Mensaje en la barra de estado
		menu_simulacion_abrir.triggered.connect(self.menuAbrirSimulacion) #Lanzador
		menu_aleatorios.addAction(menu_simulacion_abrir)

		menu_simulaciion_linea_abrir = QtWidgets.QAction(QtGui.QIcon(), "&Simulación línea de espera", self)
		menu_simulaciion_linea_abrir.setShortcut("Ctrl+s") #Atajo de teclado
		menu_simulaciion_linea_abrir.setStatusTip("Simulación línea de espera") #Mensaje en la barra de estado
		menu_simulaciion_linea_abrir.triggered.connect(self.menuAbrirSimulacionLinea) #Lanzador
		menu_aleatorios.addAction(menu_simulaciion_linea_abrir)

		menu_simulaciion_linea_abrir2 = QtWidgets.QAction(QtGui.QIcon(), "&Simulación línea de espera dos canales", self)
		menu_simulaciion_linea_abrir2.setShortcut("Ctrl+s") #Atajo de teclado
		menu_simulaciion_linea_abrir2.setStatusTip("Simulación línea de espera dos canales") #Mensaje en la barra de estado
		menu_simulaciion_linea_abrir2.triggered.connect(self.menuAbrirSimulacionLinea2) #Lanzador
		menu_aleatorios.addAction(menu_simulaciion_linea_abrir2)

		menu_regresion = QtWidgets.QAction(QtGui.QIcon(), "&Regresión Lineal", self)
		menu_regresion.setShortcut("Ctrl+s") #Atajo de teclado
		menu_regresion.setStatusTip("Regresión Lineal") #Mensaje en la barra de estado
		menu_regresion.triggered.connect(self.menuAbrirRegresion) #Lanzador
		menu_aleatorios.addAction(menu_regresion)

		
	def abrir_github(self):
		QtGui.QDesktopServices().openUrl(QtCore.QUrl('https://github.com/PabloEspana/pe_simulator'))

	def menuAbrirAleatorios(self):
		self.ventana2.show()

	def menuAbrirSimulacion(self):
		self.ventana3.show()

	def menuAbrirSimulacionLinea(self):
		self.ventana4.show()

	def menuAbrirSimulacionLinea2(self):
		self.ventana5.show()

	def menuAbrirRegresion(self):
		self.ventana6.show()

	def closeEvent(self, event): # Evitar cierre de ventana
		cerrar = QtWidgets.QMessageBox.question(self, "Salir", "¿Desea Cerrar?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if cerrar == QtWidgets.QMessageBox.Yes:
			event.accept()
		else: event.ignore()

		


if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	app.setStyle(QtWidgets.QStyleFactory.create('Fusion')) # <- Choose the style
	window = Aleatorios()
	window.show()
	sys.exit(app.exec_())