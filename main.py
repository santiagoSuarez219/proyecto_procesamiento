# Santiago Suarez Cortes - 1017269056
# Juan Camilo Morales Duran - 1005183857
# David Andres Llano Balvin - 1152219130

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import scipy
from scipy import signal

MAIN_MENU = """
1. Escalon unitario u(n)
2. Impulso unitario δ(n)
3. Exponencial

Ingrese la señal de entrada:: 
"""

ORDER_MENU = """
1. 1er orden
2. 2do orden
3. 3er orden

Seleccione el orden del sistema:: 
"""

z = sp.symbols('z')

def mostrar_menu():
    gamma = 0
    opcion = int(input(MAIN_MENU))
    if opcion == 3:
       gamma = float(input("\nIngrese valor de γ: "))
    numero_datos = int(input("Ingrese número de datos de la señal: "))
    frecuencia_muestreo = int(input("Ingrese frecuencia de muestreo (Hz): "))
    orden = int(input(ORDER_MENU))
    return numero_datos, frecuencia_muestreo, gamma, orden, opcion

def pedir_coeficientes(orden):
    cadena_a = ""
    cadena_b = ""
    for i in range(orden,-1,-1):
        if i == 0:
            cadena_a += "a_" + str(i) + ":"
            cadena_b += "b_"+ str(i) + ":"
            break
        cadena_a += "a_" + str(i) + ", "
        cadena_b += "b_"+ str(i) + ", " 
    valores_a = input(f"\nIngrese {cadena_a} ")
    valores_b = input(f"Ingrese {cadena_b} ")
    coeficientes_denominador = np.array(valores_a.split(",")).astype(int) # coeficientes del denominador
    coeficientes_numerador = np.array(valores_b.split(",")).astype(int) # coeficientes del numerador
    return coeficientes_denominador, coeficientes_numerador

def pedir_condiciones_iniciales(orden):
    condiciones_iniciales = []
    for i in range(orden):
        condiciones_iniciales.append(float(input("Ingrese y(" + str(-(i+1)) + "): ")))
    # condiciones_iniciales = np.array(condiciones_iniciales)
    return condiciones_iniciales

def contruirFuncionTransferencia(coeficientes_denominador, coeficientes_numerador):
    den_coeficientes = coeficientes_denominador
    num_coeficientes = coeficientes_numerador
    sumatoria = 0
    for i,c in enumerate(den_coeficientes):
        sumatoria += c * z**(len(den_coeficientes)-(i+1))
    denominador = sumatoria
    sumatoria = 0
    for i,c in enumerate(num_coeficientes):
        sumatoria += c * z**(len(num_coeficientes)-(i+1))
    numerador = sumatoria
    funcion_transferencia = numerador / denominador
    print("\nH(z): ")
    print(sp.printing.pretty(funcion_transferencia))
    print("\n")

def encontrarPolosYceros(coeficientes_denominador, coeficientes_numerador):
    ceros, polos, k = scipy.signal.residue(coeficientes_numerador, coeficientes_denominador)
    return ceros, polos

def estabilidadSistema(polos):
    for p in polos:
        if abs(p) > 1:
            return "Sistema inestable"
        if abs(p) == 1:
            return "Sistema marginalmente estable"
    return "Sistema estable"

def graficar_polos(polos, estabilidad_sistema):
    x = [p.real for p in polos]
    y = [p.imag for p in polos]
    theta = np.linspace(0, 2*np.pi, 100)
    x1 = np.cos(theta)
    y1 = np.sin(theta)
    plt.plot(x1, y1, linestyle='dashed')
    plt.scatter(x, y)
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title(estabilidad_sistema)
    plt.grid()
    plt.axis('equal')
    plt.savefig('polos.png')

# Respuesta de entrada cero metodo iterativo
def respuesta_entrada_cero_iterativo(ay, bj, condiciones_iniciales, n = 6):
    yz = list(condiciones_iniciales)
    for i in range(n):
        suma_ay_yz = sum(ay[j] * yz[i-j] for j in range(len(ay)))
        suma_bj_uz = sum(bj[j] * yz[i-j] for j in range(1, len(bj)))
        yz.append(suma_ay_yz - suma_bj_uz)
    return yz


# Iterativa
def respuesta_impulso_iterativo(coeficientes_numerador, coeficientes_denominador):
    u = lambda n: 1*(n >= 0)
    h = np.zeros(6, dtype=complex)  # Se especifica el tipo de dato como complejo
    r, p, k = scipy.signal.residue(coeficientes_numerador, coeficientes_denominador)
    for n in range(len(h)):
        for i, residue in enumerate(r):
            # Actualizar h[n] con la contribución de cada residuo y polo
            h[n] = h[n] + residue * p[i]**n * u(n)
    print(f'h[n] de forma iterativa es {h}')
    return h

def respuesta_impulso_analitico():
    tiempo_muestreo = numero_datos/frecuencia_muestreo
    dlti= signal.dlti(coeficientes_numerador, coeficientes_denominador, dt=tiempo_muestreo)
    t, h_analitico = signal.dimpulse(dlti)
    return t, h_analitico

def convolution(h):
    n = np.arange(numero_datos)
    u = lambda n: 1*(n >= 0)
    impulso = lambda n: 1*(n == 0)
    if opcion == 1:
        y = np.convolve(u(numero_datos), h, mode='same')
    elif opcion == 2:
        y = np.convolve(impulso(numero_datos), h, mode='same')
    elif opcion == 3:
        y = np.convolve(gamma**n, h, mode='same')
    return y


# Método iterativo
numero_datos, frecuencia_muestreo, gamma, orden, opcion= mostrar_menu()
coeficientes_denominador, coeficientes_numerador = pedir_coeficientes(orden)
condiciones_iniciales = pedir_condiciones_iniciales(orden)
contruirFuncionTransferencia(coeficientes_denominador, coeficientes_numerador)
ceros, polos = encontrarPolosYceros(coeficientes_denominador, coeficientes_numerador)
estabilidad_sistema = estabilidadSistema(polos)
print(estabilidad_sistema)
graficar_polos(polos, estabilidad_sistema)

respuesta_entrada_cero_iterativo()

h_iterativo = respuesta_impulso_iterativo(coeficientes_numerador, coeficientes_denominador)




