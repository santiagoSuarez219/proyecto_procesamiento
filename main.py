#Laboratorio 1 Procesamiento de señales
# import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import scipy

MAIN_MENU = """
Ingrese la señal de entrada:
1. Escalon unitario u(n)
2. Impulso unitario δ(n)
3. Exponencial

Dato ingresado: 
"""

ORDER_MENU = """
Seleccione el orden del sistema:

1. 1er orden
2. 2do orden
3. 3er orden

Dato ingresado: 
"""

z = sp.symbols('z')

def menu():
    gamma = 0
    # opcion = int(input(MAIN_MENU))
    # if opcion == 3:
    #    gamma = float(input("\nIngrese valor de γ: "))
    #numeroDatos = int(input("Ingrese número de datos de la señal: "))
    #frecuenciaMuestreo = int(input("Ingrese frecuencia de muestreo (Hz): "))
    orden = int(input(ORDER_MENU))
    #return opcion, numeroDatos, frecuenciaMuestreo, gamma, orden
    return orden


def coeficientes(orden):
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
    coeficientes_a = tuple(valores_a.split(",")) # coeficientes del denominador
    coeficientes_b = tuple(valores_b.split(",")) # coeficientes del numerador
    return coeficientes_a, coeficientes_b

def condicionesIniciales(orden):
    condiciones_iniciales = []
    for i in range(orden):
        condiciones_iniciales.append(float(input("Ingrese y(" + str(-(i+1)) + "): ")))
    condiciones_iniciales = tuple(condiciones_iniciales)
    return condiciones_iniciales

def contruirFuncionTransferencia(coeficientes_a, coeficientes_b):
    den_coeficientes = coeficientes_a
    num_coeficientes = coeficientes_b
    sumatoria = 0
    for i,c in enumerate(den_coeficientes):
        sumatoria += int(c) * z**(len(den_coeficientes)-(i+1))
    denominador = sumatoria
    sumatoria = 0
    for i,c in enumerate(num_coeficientes):
        sumatoria += int(c) * z**(len(num_coeficientes)-(i+1))
    numerador = sumatoria

        

    # numerador = sum(int(c) * z**(len(num_coeficientes)-(i+1)) for i, c in enumerate(num_coeficientes))
    # denominador = sum(int(c) * z**(len(num_coeficientes)-i+1) for i, c in enumerate(den_coeficientes))
    funcion_transferencia = numerador / denominador
    print("\nH(z): ")
    print(sp.printing.pretty(funcion_transferencia))
    print("\n")

def encontrarPolosYceros(coeficientes_a, coeficientes_b):
    ceros, polos, k = scipy.signal.residue(coeficientes_b, coeficientes_a)
    return ceros, polos

def estabilidadSistema(polos):
    for p in polos:
        if abs(p) > 1:
            return "Sistema inestable"
        if abs(p) == 1:
            return "Sistema marginalmente estable"
    return "Sistema estable"

def graficaPolos(polos, estabilidad_sistema):
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


def main ():
    orden = menu()
    coeficientes_a, coeficientes_b = coeficientes(orden)
    # condiciones_iniciales = condicionesIniciales(orden)
    contruirFuncionTransferencia(coeficientes_a, coeficientes_b)
    ceros, polos = encontrarPolosYceros(coeficientes_a, coeficientes_b)
    estabilidad_sistema = estabilidadSistema(polos)
    print(estabilidad_sistema)
    graficaPolos(polos, estabilidad_sistema)


if __name__ == "__main__":
    main()