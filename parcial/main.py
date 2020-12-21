'''
Pida el ingreso de n[8,12] y genere aleatoriamente npares ordenados. 
El programa debemostrar gráficamente la curva que se aproxime mejor linealmente a los npares ordenados. 
El usuario debe seleccionar el tipo de curva: polinomial(de grado 𝑚≤6), exponencial o potencial.

# TO DO:
- Click en el plano para añadir puntos

'''

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as pltback
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import regresion

# ----------- GLOBALES ------------------------------------------------------------------------------
funcionesNombres = ["Regresión Lineal", "Regresión Polinomial", "Regresión Potencial", "Regresión Exponencial"]

valores, curvasFunciones  = [[],[]], []
graph, toolbar = None, None
numeroPares, ordenado, grado, dibujado = None, None, None, False

# ----------- FUNCIONES -----------------------------------------------------------------------------
def dibujar(primer=False):
	global graph, toolbar, valores, curvasFunciones, dibujado

	# Reiniciar la gráfica
	if dibujado:
		graph.get_tk_widget().grid_remove()
		toolbar.grid_remove()
	if not dibujado and not primer:
		dibujado = True

	# Figure
	figure = plt.figure(figsize=(5,4),dpi=125) 
	figure.add_axes([1,1,1,1])
	subplot = figure.add_subplot(111)
	
	# Graficar las curvas
	subplot.plot(valores[0],valores[1],'ro')
	for i in range(len(curvasFunciones)):
		subplot.plot(curvasFunciones[i][1][0], curvasFunciones[i][1][1], label=curvasFunciones[i][0])
		#subplot.set_title(curvasFunciones[i][1][2], fontsize = 'x-small')

	# Subplot Config
	subplot.legend(fontsize = 'xx-small')
	subplot.grid()
	subplot.spines['left'].set_position('zero')
	subplot.spines['right'].set_color('none')
	subplot.spines['bottom'].set_position('zero')
	subplot.spines['top'].set_color('none')
	subplot.set_xlim(0, 21)
	subplot.set_ylim(0, 21)
	subplot.xaxis.set_ticks(list(range(22)))
	subplot.yaxis.set_ticks(list(range(22)))
	
	# Mostrar Graficos
	graph = pltback.FigureCanvasTkAgg(figure, master=window)
	canvas.create_window(550, 275, window=graph.get_tk_widget())
	toolbar = tk.Frame(master=window)
	canvas.create_window(550, 550, window=toolbar)
	pltback.NavigationToolbar2Tk(graph, toolbar)

def generar():
	global valores, curvasFunciones, numeroPares, ordenado, dibujado
	n, o = escalaCantidad.get(), seleccionarOrden.get()

	# Revisa si X y Y existen o si se pide otra cantidad de pares en el slider
	if n != numeroPares or o != ordenado:
		# Actualizar los valores
		numeroPares, ordenado = n, o

		# Limpiar listas y generar los valores
		valores, curvasFunciones = [[],[]] , []
		valores = regresion.generar(numeroPares, ordenado)

		# Etiqueta cantidad de numeros
		labelCantidad = tk.Label(window,text="Cantidad de pares: "+str(len(valores[0])),anchor="w",justify="left")
		canvas.create_window(76,15,window=labelCantidad)

		# Activar para graficas
		botonGraficar.config(state="normal")
		escalaGrado.config(state="normal")
		menuFunciones.config(state="normal")

		# Limpiar cuadro list de inecuaciones
		widgetEcuaciones.configure(state="normal")
		widgetEcuaciones.delete("1.0","end")
		widgetEcuaciones.configure(state="disable") 

		# Dibujar las curvas
		dibujar()
		
def graficar():
	global graph, toolbar
	global grado, valores, dibujado
	grado = escalaGrado.get()

	titulo, funcion = None, None
	if menuFunciones.get() == funcionesNombres[0]:
		titulo = menuFunciones.get()
		funcion = regresion.regresionLineal(valores)
	elif menuFunciones.get() == funcionesNombres[1]:
		titulo = menuFunciones.get() + " (Grado " + str(grado) + ")"
		funcion = regresion.regresionPolinomial(valores, grado)
	elif menuFunciones.get() == funcionesNombres[2]:
		titulo = menuFunciones.get()
		funcion = regresion.regresionPotencial(valores)
	elif menuFunciones.get() == funcionesNombres[3]:
		titulo = menuFunciones.get()
		funcion = regresion.regresionExponencial(valores)
	curvasFunciones.append([titulo,funcion])

	# Agregar al cuadro
	widgetEcuaciones.config(state="normal")
	widgetEcuaciones.insert("insert",titulo+"\n"+funcion[2]+"\n-----------\n")
	widgetEcuaciones.config(state="disable")

	# Dibujar las curvas
	dibujar()
	
# ----------- INTERFAZ ------------------------------------------------------------------------------
# Window (root)
window = tk.Tk()
window.title("Regresiones")
window.config(bg="SystemButtonFace")

# Canvas
canvas = tk.Canvas(window, width=875, height=575)
canvas.grid()

# Dibujar el canvas en blanco por primera vez
dibujar(True)

# Etiqueta cantidad de numeros
labelCantidad = tk.Label(window,text="Cantidad de pares:     ",anchor="w",justify="left")
canvas.create_window(76,15,window=labelCantidad)

# Escala para los numeros de pares ordenados que vamos a tener
escalaCantidad = tk.Scale(canvas,from_=8,to=12,length=200,digits=1,resolution=1,orient="horizontal",label="Numero de Pares")
canvas.create_window(115,60,window=escalaCantidad)

# Checkbox para ordenar los pares del Y
seleccionarOrden = tk.IntVar()
checkboxOrden = tk.Checkbutton(canvas,text="Ordenado",variable=seleccionarOrden)
canvas.create_window(175,43,window=checkboxOrden)
checkboxOrden.select()

# Boton para generar los pares ordenados
botonGenerar = tk.Button(canvas,text="Generar Aleatoriamente",command=generar,bg="orange")
canvas.create_window(115,110,window=botonGenerar)

# Etiqueta cantidad de numeros
labelFunciones = tk.Label(window,text="Seleccione la funcion:",anchor="center")
canvas.create_window(79,160,window=labelFunciones)

# Menu combobox de funciones
seleccionarFuncion = tk.StringVar()
menuFunciones = ttk.Combobox(canvas,textvariable=seleccionarFuncion,values=funcionesNombres)
menuFunciones.current(0)
menuFunciones.config(state="disable")
canvas.create_window(115,185,window=menuFunciones, width=200)

# Escala para medir el grado polinomial que va desde 2 a 6
escalaGrado = tk.Scale(canvas,from_=2,to=6,length=200,digits=1,resolution=1,orient="horizontal",label="Grado Polinomial")
escalaGrado.config(state="disable")
canvas.create_window(115,230,window=escalaGrado)

# Boton para generar los pares ordenados
botonGraficar = tk.Button(canvas,text="Graficar",command=graficar,bg="light green")
botonGraficar.config(state="disable")
canvas.create_window(115,280,window=botonGraficar)

# Etiqueta cantidad de numeros
labelLista = tk.Label(window,text="Lista de ecuaciones:",anchor="w",justify="left")
canvas.create_window(73,310,window=labelLista)

# Text Widget lista de ecuaciones
widgetEcuaciones = tk.Text(window,width=24,height=10,padx=5,pady=5,bg='SystemButtonFace',state="disable")
canvas.create_window(115,410, window=widgetEcuaciones)

# Loop Principal
window.mainloop()