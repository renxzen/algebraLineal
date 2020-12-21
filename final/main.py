'''
Programacion Lineal
Pida el ingreso de una función lineal de la forma f(x, y) = ax + by
y de n inecuaciones lineales (nE[3, 8]) que formen un polígono D
(acotado o no). El programa debe determinar el valor mínimo y
máximo de la función sobre el conjunto D (en caso existan).

# TO DO:
- REWORK

'''

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import extract as ext

# ----------- INICIAR TKINTER ------------------------------------------------------------------------------
# Window (root)
window = tk.Tk()
window.title("Programacion Lineal")
window.config(bg="SystemButtonFace")

# Canvas
canvas = tk.Canvas(window, width=300, height=600)
canvas.grid()

# Figure
figure = plt.figure(figsize=(5,4),dpi=130) 
subplot = figure.add_subplot(111)

# Gráfico
graph = FigureCanvasTkAgg(figure, master=window)
graph.get_tk_widget().grid(row=0, column=1)

# Mostrar toolbar
toolbar = tk.Frame(master=window)
toolbar.grid(row=1,column=1)
NavigationToolbar2Tk(graph, toolbar)

# ----------- GLOBALES ------------------------------------------------------------------------------
# Arreglos de las inecuaciones
inecuacionesLista, rectas, parametros = [], [], []
intersecciones, funcionObjetivo, poligono = [], [], []
respuesta, respuestaFormateada = [], []

# Textos Default
textoEjemploInecuacion = "Ejemplo: 2x-1.5y<=2"
textoEjemploFuncionObjetivo = "Ejemplo: 3x + 7y"

# ----------- FUNCIONES ------------------------------------------------------------------------------
def startLP():
	global funcionObjetivo
	entrada = textboxFunc.get()

	try:
		# Leer la funcion objetivo y guardar
		xi, yi, _, _, _ = ext.stripString(entrada)
		funcionObjetivo = [xi,yi]

		# Desactivar la escritura del Textbox funcion objetivo
		textboxFunc.configure(state="disabled")

		# Activa la escritura de Inecuaciones
		textboxAdd.config(state="normal")
		buttonAdd.config(state="normal")
	except:
		print("Funcion objetivo invalida")


def addInecuation():
	global graph, inecuacionesLista, parametros, rectas
	entrada = textboxAdd.get()

	try:
		# Agregar a la lista de string
		inecuacionesLista.append(entrada)

		# Agregar a la lista de parametros
		xi, yi, ri, si, ei = ext.stripString(entrada)
		parametros.append([xi,yi,ri,si,ei])

		# Agregar a la lista de lineas para graficas
		curvai = ext.generateLine(xi,yi,ri)
		rectas.append(curvai)

		# Generar Grafico
		generarGrafico()

		# Quitar los espacios
		entrada = entrada.replace(" ", "")

		# Agregar al cuadro
		cuadroIneq.config(state="normal")
		cuadroIneq.insert("insert",entrada+"\n")
		cuadroIneq.config(state="disable")

		# Eliminar del textbox de inecuaciones
		textboxAdd.delete(0,"end")
	except:
		print("Inecuacion invalida")


def generarGrafico():
	global graph, toolbar, rectas, intersecciones
	global poligono, funcionObjetivo, respuesta, respuestaFormateada

	# Reiniciar la gráfica
	graph.get_tk_widget().grid_remove()
	toolbar.grid_remove()
	
	# Iniciar Figure
	figure = plt.figure(figsize=(5,4),dpi=130) 
	figure.add_axes([1,1,1,1])
	subplot = figure.add_subplot(111)

	# Graficar cada curva
	for i in range(len(inecuacionesLista)):
		subplot.plot(rectas[i][0], rectas[i][1], '--', label=inecuacionesLista[i])

	# Encontrar las intersecciones y el poligono
	intersecciones = ext.findIntersections(parametros)
	poligono = ext.getPolygon(parametros, intersecciones)
	
	# Graficar los vertices del poligono
	for i, j in zip(poligono[0],poligono[1]):
		plt.plot(i,j,color='black', marker='o',markersize=6)

	# Graficar el area del poligono
	plt.fill(poligono[0],poligono[1],'red',alpha=0.5)

	# Obtener funcion objetivo
	try:
		respuesta = ext.getAnswer(funcionObjetivo,poligono)
		respuestaFormateada = ext.formatAnswer(funcionObjetivo,respuesta)

		# Añadir el minimo al recuadro
		textboxMin.config(state="normal")
		textboxMin.delete("1.0","end")
		textboxMin.insert("insert",respuestaFormateada[0])
		textboxMin.config(state="disabled")

		# Añadir el maximo al recuadro
		textboxMax.config(state="normal")
		textboxMax.delete("1.0","end")
		textboxMax.insert("insert",respuestaFormateada[1])
		textboxMax.config(state="disabled")
	except:
		pass

	# Configuracion del subplot
	#subplot.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
	subplot.legend()
	subplot.grid()
	subplot.spines['left'].set_position('zero')
	subplot.spines['right'].set_color('none')
	subplot.spines['bottom'].set_position('zero')
	subplot.spines['top'].set_color('none')

	# Configurar limites del subplot
	xMax, yMax = ext.getMargins(intersecciones)
	subplot.set_xlim(-5,xMax)
	subplot.set_ylim(-5,yMax)

	# Gráfico
	graph = FigureCanvasTkAgg(figure, master=window)
	graph.get_tk_widget().grid(row=0, column=1)
	
	# Mostrar toolbar
	toolbar = tk.Frame(master=window)
	toolbar.grid(row=1,column=1)
	NavigationToolbar2Tk(graph, toolbar)


def reset():
	global graph, toolbar, inecuacionesLista, rectas, parametros
		
	# Limpiar textbox de funcion objetivo
	textboxFunc.configure(state="normal")
	textboxFunc.delete(0,"end")
	textboxFunc.insert(0, textoEjemploFuncionObjetivo)

	# Limpiar textbox de inecuaciones
	textboxAdd.delete(0,"end")
	textboxAdd.insert(0,textoEjemploInecuacion)
	textboxAdd.config(state="disable")  

	# Limpiar cuadro list de inecuaciones
	cuadroIneq.configure(state="normal")
	cuadroIneq.delete("1.0","end")
	cuadroIneq.configure(state="disable") 

	# Desactivar el boton de Añadir
	buttonAdd.config(state="disable") 

	# Borrar el minimo del recuadro
	textboxMin.config(state="normal")
	textboxMin.delete("1.0","end")
	textboxMin.config(state="disabled")

	# Borrar el maximo del recuadro
	textboxMax.config(state="normal")
	textboxMax.delete("1.0","end")
	textboxMax.config(state="disabled")

	# Limpiar las listas
	inecuacionesLista.clear()   
	rectas.clear()
	parametros.clear()
	intersecciones.clear()
	funcionObjetivo.clear()
	poligono.clear()
	respuesta.clear()
	respuestaFormateada.clear()

	# Remover los graficos y la barra de herramientas
	graph.get_tk_widget().grid_remove()
	toolbar.grid_remove()   


# ----------- INTERFAZ ------------------------------------------------------------------------------
# Etiqueta Funcion Objetivo
labelFunc = tk.Label(window, text="Ingrese funcion objetivo:")
labelFunc.config(font=("Consolas",15))
canvas.create_window(150, 10, window=labelFunc)

# Textbox Funcion Objetivo
textboxFunc = ttk.Entry(window, justify="center", font=("Consolas",15))
textboxFunc.insert(0, textoEjemploFuncionObjetivo)
canvas.create_window(150, 40, window=textboxFunc)

# Boton Estabecer Funcion Objetivo
buttonSet = tk.Button(window, text="Establecer",command=startLP, bg='palegreen', font=("Consolas",15)) 
canvas.create_window(150, 80, window=buttonSet)

# Etiqueta Inecuaciones
labelAdd = tk.Label(window, text="Ingrese inecuaciones:")
labelAdd.config(font=("Consolas",15))
canvas.create_window(150, 125, window=labelAdd)

# Textbox Añadir Inecuacion
textboxAdd = ttk.Entry(window, justify="center", font=("Consolas",15))
textboxAdd.insert(0, textoEjemploInecuacion)
textboxAdd.config(state="disabled")
canvas.create_window(150, 155, window=textboxAdd)

# Boton Añadir Inecuacion
buttonAdd = tk.Button(window, text="Añadir",command=addInecuation, bg='palegreen', font=("Consolas",15))
buttonAdd.config(state="disable")
canvas.create_window(150, 195, window=buttonAdd)

# Text Widget Lista de Inecuaciones
cuadroIneq = tk.Text(window, width=22, height=8, padx=5, pady=5,bg='SystemButtonFace', font=("Consolas",15), state="disable")
canvas.create_window(150, 320, window=cuadroIneq)

# Etiqueta Minimo
labelMin = tk.Label(window, text="Funcion objetivo minima:")
labelMin.config(font=("Consolas",13))
canvas.create_window(150, 435, window=labelMin)

# Textbox Añadir Funcion Objetiva Minima
textboxMin = tk.Text(window, width=32, height=1, padx=3, pady=3,bg='SystemButtonFace', font=("Consolas",11), state="disable")
canvas.create_window(150, 460, window=textboxMin)

# Etiqueta Maximo
labelMax = tk.Label(window, text="Funcion objetivo maxima:")
labelMax.config(font=("Consolas",13))
canvas.create_window(150, 490, window=labelMax)

# Textbox Añadir Funcion Objetiva Maxima
textboxMax = tk.Text(window, width=32, height=1, padx=3, pady=3,bg='SystemButtonFace', font=("Consolas",11), state="disable")
textboxMax.config(state="disabled")
canvas.create_window(150, 515, window=textboxMax)

# Boton Reiniciar
buttonReset = tk.Button(window, text="Reiniciar",command=reset, bg='pink', font=("Consolas",15)) 
canvas.create_window(150, 565, window=buttonReset)

# Loop Principal
window.mainloop()