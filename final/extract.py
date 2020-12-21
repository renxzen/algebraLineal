import random as rnd
import numpy as np
import math


def stripString(text):
	# Revisar si el string esta vacio
	x = text[0]

	# Quitar los espacios
	text = text.replace(" ", "")

	# Obtener la posicion del <, > o =
	idr = max(text.find("<"), text.find(">"), text.find("="))
	x, y, r = 0, 0, 0

	# Obtener x si esta presente
	if (idx:=text.find("x")) >= 0:
		start = max(text[:idx].rfind("y"),
					text[:idx].rfind("<"),
					text[:idx].rfind(">"),
					text[:idx].rfind("="))
		x = text[start+1:idx]
		if x == "" or x == "+": x = 1
		if x == "-": x = -1
		if idx > idr and idr != -1: x = -1 * int(x)
		else: x = float(x)

	# Obtener y si esta presente
	if (idy:=text.find("y")) >= 0:
		start = max(text[:idy].rfind("x"),
					text[:idy].rfind("<"),
					text[:idy].rfind(">"),
					text[:idy].rfind("="))
		y = text[start+1:idy]
		if y == "" or y == "+": y = 1
		if y == "-": y = -1
		if idy > idr and idr != -1: y = -1 * int(y)
		else: y = float(y)

	# Obtener la respuesta
	if idr > idx and idr > idy:
		r = float(text[idr+1:])

	# Obtener la orientacion # 0 Menor"<" | 1 Mayor">"
	s = int(text.find(">")>0)

	# Obtener si hay igual o no # 0 No | 1 Si
	e = max(0,int(text.find("=")>0))

	return x, y, r, s, e


def generateLine(x, y, r, minVal = -1000, maxVal = 1000):
	xr = np.linspace(minVal, maxVal, 20)
	yr = np.linspace(minVal, maxVal, 20)
	if x == 0 and y != 0:
		# En el caso de que se tenga que graficar una linea horizontal
		yr = np.repeat(r, 20)
	elif y == 0 and x != 0:
		# En el caso de que se tenga que graficar una linea vertical
		xr = np.repeat(r, 20)
	else:
		# Graficar la recta normalmente
		yr = (r-x*xr)/y
	return xr, yr


def findIntersections(parameters):
	# Se utiliza un set para evitar repeticiones
	intersections = set()

	# Intersecciones entre las lineas
	for i in parameters:
		for j in parameters:
			if i != j:
				xi, yi, ri, _, _ = i
				xj, yj, rj, _, _ = j
				try:
					# Se igualan las ecuaciones para hallar las intersecciones
					xr = (ri*yj - rj*yi)/(xi*yj - xj*yi)
					yr = (ri*xj - rj*xi)/(yi*xj - yj*xi)

					# Evitar que hayan intersecciones negativas
					if xr >= 0 and yr >= 0:
						intersections.add((xr,yr))
				except:
					# Se ignora si existe una division por cero (error)
					pass
	
	# Intersecciones con los ejes
	for i in parameters:
		xi, yi, ri, _, _ = i
		xr, yr = 0, 0

		# Coordenada (x,0)
		if xi != 0:
			xr = ri/xi
			intersections.add((xr,0))
		# Coordenada (0,y)
		if yi != 0:
			yr = ri/yi
			intersections.add((0,yr))
		
	# Añadir el origen como interseccion para graficar
	intersections.add((0,0))

	# Se devuelve el set convertido a lista
	return list(intersections)


def getPolygon(parameters, intersections):
	polygon = []

	# Se evalua cada punto de interseccion
	for x, y in intersections:
		check = 0

		# Se evalua cada parametro de la inecuacion
		for p in parameters:
			xi, yi, ri, si, ei = p

			# Comparaciones previas
			value = x*xi + y*yi - ri
			positivo = int(value > 0)
			cero = int(value == 0)

			# Compara las comparaciones con los parametros 
			if si == positivo or ei == cero:
				check += 1

		# Si cumple con todas las inecuaciones, se agrega
		if check == len(parameters):
			polygon.append((x,y))

	# Ordenar los vertices del poligono para su correcta graficacion con plt.fill
	# Calcular el centroide del poligono
	xPoints = [point[0] for point in polygon]
	yPoints = [point[1] for point in polygon]
	centroX = sum(xPoints)/len(polygon)
	centroY = sum(yPoints)/len(polygon)

	# Calcular el angulo relativo de cada punto con respecto al centro
	angles = []
	for i in polygon:
		angle = math.atan2(i[1]-centroY,i[0]-centroX) + math.pi
		angles.append((angle,i[0],i[1]))

	# Ordenar el arreglo segun el angulo
	angles.sort()

	# Dividir la lista en dos para graficar con fill
	xAux = [point[1] for point in angles]
	yAux = [point[2] for point in angles]
	polygon = [xAux, yAux]

	return polygon


def getAnswer(objFunction, polygon):
	mini, maxi = 1e9, 0
	maxResult, minResult = [0]*3, [0]*3
	
	# Iterar por cada valor X y Y del poligono
	for xi, yi in zip(polygon[0],polygon[1]):
		result = objFunction[0]*xi + objFunction[1]*yi
		
		# Encontrar los valores minimos y maximos de la funcion objetivo
		if result < mini:
			minResult[0], minResult[1] = xi, yi
			minResult[2], mini = result, result
		if result > maxi:
			maxResult[0], maxResult[1] = xi, yi
			maxResult[2], maxi = result, result

	return [minResult, maxResult]

def formatAnswer(objFunction, answer):
	formattedAnswer = [0,0]

	# Revisar si el cociente de Y es negativo o positivo
	for i in range(len(answer)):
		sign = ""
		if answer[i][1] < 0:
			sign = "-"
		else:
			sign = "+"

		# Redondear a dos decimales 
		formattedAnswer[i] = ("{}*{} ").format(objFunction[0],round(answer[i][0],2)) + sign + (" {}*{} = {}").format(objFunction[1],round(abs(answer[i][1]),2),round(answer[i][2],2))

	return formattedAnswer

def getMargins(intersections, pad = 15):
	xMax, yMax = 0, 0

	# Encontrar los valores mayores de cada eje
	for i in intersections:
		xMax = max(xMax, i[0])
		yMax = max(yMax, i[1])

	# Aplicar el margen pad o reemplazar por 20 si es 0
	xMax = max(xMax+pad, 20)
	yMax = max(yMax+pad, 20)

	return xMax, yMax

if __name__ == "__main__":
	pruebas = ["2x + 3y <= 9",
		"-2x - 4y > 4",
		"x + y < 1",
		"x > -9",
		"y <= 0",
		"x > y",
		"y <= x",
		"y > 3x",
		"-3y <= -2x",
		"-7x > -10y",
		"-y > -x",
		"-x > -y",
		"-x <= 3",
		"y - x < 4"
	]

	for i in pruebas:
		print("---------\n",i,": \n",stripString(i),sep="")
