import numpy as np
import math
import random

def generar(n,order):	
	X =  list(range(1, 21))
	for i in range(20-n):
		del X[random.randint(0, len(X)-1)]
	Y = [0]*n
	for i in range(n):
		Y[i] = random.randint(1, 20)
	if order:
		Y.sort()
	return [X,Y]

def regresionLineal(valores):
	A = np.array([[i, 1] for i in valores[0]])
	B = np.array([[i] for i in valores[1]])
	LiR = np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.dot(np.transpose(A), B))
	
	ejeX =  np.arange(0, 21, 0.1)
	ejeY = LiR[0]*ejeX+LiR[1] #y = ax + b
	descripcion = "y = " + str(round(float(LiR[0]),5)) + "x + " + str(round(float(LiR[1]), 5))
	respuesta = [ejeX,ejeY,descripcion]
	return respuesta


def regresionPolinomial(valores, G):
	A = np.array([[pow(j, i) for i in range(G, -1, -1)] for j in valores[0]])
	B = np.array([[i] for i in valores[1]])
	PoR = np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.dot(np.transpose(A), B))
		
	ejeX =  np.arange(0, 21, 0.1)
	ejeY = 0 #y = a1*x^n + a2*x^n-1 + ... + an*x^0
	descripcion = "y = "
	j = 0
	for i in range(G, -1, -1):
		ejeY += PoR[j] * pow(np.array(ejeX), i)
		if i > 1:
			descripcion += str(round(float(PoR[j]),5)) + "x^" + str(i) + " + "
		elif i == 1:
			descripcion += str(round(float(PoR[j]),5)) + "x  + "
		else:
			descripcion += str(round(float(PoR[j]),5))
		j += 1
	respuesta = [ejeX,ejeY,descripcion]
	return respuesta


def regresionPotencial(valores):
	A = np.array([[1, math.log(i)] for i in valores[0]])
	B = np.array([[math.log(i)] for i in valores[1]])
	PtR = np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.dot(np.transpose(A), B))
	PtR[0] = pow(math.e, PtR[0])
	
	ejeX =  np.arange(0, 21, 0.1)
	ejeY = PtR[0]*pow(ejeX, PtR[1]) #y = ax^b
	descripcion = "y = " + str(round(float(PtR[0]), 5)) + "x^" + str(round(float(PtR[1]), 5))
	respuesta = [ejeX,ejeY,descripcion]
	return respuesta


def regresionExponencial(valores):
	A = np.array([[1, i] for i in valores[0]])
	B = np.array([[math.log(i)] for i in valores[1]])
	ExR = np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.dot(np.transpose(A), B))
	ExR[0] = pow(math.e, ExR[0])
	
	ejeX =  np.arange(0, 21, 0.1)
	ejeY = ExR[0]*pow(math.e, ExR[1]*ejeX) #y = ae^(bx)
	descripcion = "y = " + str(round(float(ExR[0]),5)) + "e^(" + str(round(float(ExR[1]),5)) + "x)"
	respuesta = [ejeX,ejeY,descripcion]
	return respuesta
