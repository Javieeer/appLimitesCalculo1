import sympy
import numpy as np
import matplotlib.pyplot as plt
import re
from tkinter import *
from tkinter import messagebox

# Definir la variable simbólica 'x' de SymPy
x = sympy.symbols('x')

# Función para calcular el límite y proceso paso a paso
def calcular_limite(funcion, variable, punto):
    """ Calcula el límite de una función en un punto dado y devuelve el proceso paso a paso. """
    proceso = []
    
    # Paso 1: Mostrar la función original (como fue ingresada)
    funcion_original = funcion 
    proceso.append(f"\nFunción original:\n{formatear_fraccion(funcion_original)}\n")
    
    # Paso 2: Factorización de la función (si es posible)
    funcion_factorizada = sympy.factor(funcion)
    proceso.append(f"Función factorizada:\n{formatear_fraccion(funcion_factorizada)}\n")
    
    # Paso 3: Calcular el límite
    limite = sympy.limit(funcion, variable, punto)
    limite = round(limite, 2)  
    
    return limite, proceso

# Función para formatear fracciones visualmente
def formatear_fraccion(expresion):
    """ Toma una expresión simbólica de SymPy y la convierte a un formato visual tipo fracción. """
    if isinstance(expresion, sympy.Rational) or isinstance(expresion, sympy.Mul):
        numerador, denominador = expresion.as_numer_denom()
        
        # Convertir el numerador y denominador a cadenas de texto
        numerador = str(numerador)
        denominador = str(denominador)
        
        # Formatear el numerador y denominador con la barra divisoria
        return f"    {numerador}\n{'-' * 20}\n{denominador}"
    
    if isinstance(expresion, sympy.Pow):
        base, exponente = expresion.args
        if exponente < 0:  # Si el exponente es negativo, estamos ante una fracción
            numerador = 1
            denominador = base**(-exponente)  # Convertir el exponente negativo a positivo
            return f"    {numerador}\n{'-' * 20}\n{denominador}"
    
    # Si no es fracción, simplemente retornamos la expresión como está
    return str(expresion)

# Función para graficar la función
def graficar_funcion(funcion, variable, punto):
    """ Grafica la función y marca el límite en el punto especificado. """
    # Comprobar si ya hay una figura abierta y cerrarla si es necesario
    plt.clf()  # Limpiar la figura actual
    plt.close()  # Cerrar la ventana actual del gráfico
    
    # Convertir la función a una forma que pueda ser evaluada numéricamente
    f_lambdified = sympy.lambdify(variable, funcion, 'numpy')
    
    # Generar valores para la gráfica
    x_vals = np.linspace(punto - 10, punto + 10, 300, endpoint=True, dtype=float)
    
    # Filtrar los valores de x_vals que no conduzcan a una división por cero
    y_vals = []
    for val in x_vals:
        try:
            # Intentar evaluar la función en cada valor de x
            y = f_lambdified(val)
            # Si el valor es muy grande (para evitar divisiones por cero), asignamos NaN
            if np.abs(y) > 1e10:  # Umbral de tolerancia para valores muy grandes
                y_vals.append(np.nan)
            else:
                y_vals.append(y)
        except ZeroDivisionError:
            y_vals.append(np.nan)  # Si hay una división por cero, asignar NaN
    
    # Crear la gráfica
    plt.plot(x_vals, y_vals, label=str(funcion))
    
    # Asegurarse de que el valor del límite es visible en la gráfica
    try:
        limite = sympy.limit(funcion, x, punto)
        # Convertir el límite en valor numérico para mostrarlo en la gráfica
        limite_valor = float(limite)
        
        # Marcar el límite en el gráfico
        plt.scatter([punto], [limite_valor], color='red', zorder=5, label=f'Limite en x={punto} ({limite_valor})')
    except ZeroDivisionError:
        pass  # Si ocurre una división por cero al marcar el límite, no mostrar el punto
    except Exception as e:
        print(f"Error al calcular el límite para graficar: {e}")
    
    # Etiquetas y título
    plt.axvline(x=punto, color='gray', linestyle='--', label=f'x={punto}')
    plt.axhline(0, color='black',linewidth=1)
    plt.axvline(0, color='black',linewidth=1)
    plt.title(f'Gráfica del límite en x={punto}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para obtener los datos de entrada
def obtenerDatos(entrada_funcion, entrada_punto):
    
    """ Obtiene los datos de entrada, los procesa y los devuelve. """
    # Obtener la función ingresada, reemplazando ^ por ** y 3x por 3*x
    funcion_str = entrada_funcion.get()
    funcion_str = funcion_str.replace("^", "**")
    
    # Reemplazar la multiplicación implícita, como '3x' por '3*x'
    funcion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_str)

    # Convertir la cadena a una función simbólica
    funcion = sympy.sympify(funcion_str)
    
    # Obtener el punto de entrada
    punto = round(float(entrada_punto.get()), 2)  # Redondear el punto a 2 decimales
    
    return funcion, punto

# Función que se ejecuta cuando se hace clic en el botón "Calcular Límite"
def obtener_limite(entrada_funcion, entrada_punto, resultado_text):
    try:
        funcion, punto = obtenerDatos(entrada_funcion, entrada_punto)  # Llamar para obtener la función y el punto
        # Calcular el límite y obtener el proceso paso a paso
        limite, proceso = calcular_limite(funcion, x, punto)
        
        # Limpiar el Text widget antes de mostrar el nuevo proceso
        resultado_text.config(state=NORMAL)
        resultado_text.delete(1.0, END)  # Limpiar cualquier texto anterior
        
        # Mostrar el resultado del límite y el proceso paso a paso
        resultado_text.insert(INSERT, f"El límite cuando x tiende a {punto} es: {limite}\n\nProceso:\n")
        for paso in proceso:
            resultado_text.insert(INSERT, f"{paso}\n")
        
        # Deshabilitar la edición del Text widget
        resultado_text.config(state=DISABLED)
        
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error al calcular el límite o graficar la función.\n" + str(e) + "\nVerifique la función ingresada y el punto.")

# Función para graficar el límite
def dibujar_limite(entrada_funcion, entrada_punto):
    try:
        funcion, punto = obtenerDatos(entrada_funcion, entrada_punto)  # Llamar para obtener la función y el punto
        graficar_funcion(funcion, x, punto)  # Graficar la función
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error al calcular el límite o graficar la función.\n" + str(e) + "\nVerifique la función ingresada y el punto.")

# Configuración de la ventana principal
root = Tk()
root.title("Programa Limites de Javier")
root.geometry("505x500")

# ETIQUETAS Y ENTRADAS
etiqueta_funcion = Label(root, text="Ingresa la función (ej. 3x^2 + 2x - 1): ")
etiqueta_funcion.grid(row=0, column=0, padx=5, pady=5, sticky="e") 

entrada_funcion = Entry(root, width=45)
entrada_funcion.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

etiqueta_punto = Label(root, text="Valor al que tiende x: ")
etiqueta_punto.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entrada_punto = Entry(root, width=45)
entrada_punto.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# BOTONES
boton_calcular = Button(root, text="Calcular Límite", command=lambda: obtener_limite(entrada_funcion, entrada_punto, resultado_text))
boton_calcular.grid(row=2, column=0, pady=10)

boton_graficar = Button(root, text="Graficar Límite", command=lambda: dibujar_limite(entrada_funcion, entrada_punto))
boton_graficar.grid(row=2, column=1, pady=10)

# PROCESO DE SOLUCIÓN
resultado_text = Text(root, width=70, height=20, font=("Helvetica", 10), wrap=WORD, bg="lightyellow")
resultado_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
resultado_text.config(state=DISABLED)  # Deshabilitar edición

# Ejecutar la interfaz gráfica
root.mainloop()
