import sympy
import numpy as np
import matplotlib.pyplot as plt
import re
from tkinter import *
from tkinter import messagebox

x = sympy.symbols('x')

# Función para calcular el límite y proceso paso a paso
def calcular_limite(funcion, variable, punto):
    proceso = []

    # Paso 1: Mostrar la función original
    funcion_original = funcion
    proceso.append(f"\nFunción original:\n{formatear_fraccion(funcion_original)}\n")

    # Paso 2: Verificar si hay indeterminación
    numerador, denominador = funcion.as_numer_denom()
    num_val = numerador.subs(variable, punto)
    den_val = denominador.subs(variable, punto)

    if num_val == 0 and den_val == 0:
        proceso.append("Se detecta una indeterminación 0/0. Se intentará simplificar la función.\n")

    # Paso 3: Simplificar la función
    funcion_simplificada = sympy.simplify(funcion)
    proceso.append(f"Función simplificada:\n{formatear_fraccion(funcion_simplificada)}\n")

    # Paso 4: Calcular el límite
    try:
        # Intentar simplificar la expresión antes de calcular el límite
        funcion_simplificada = sympy.simplify(funcion)
        
        # Calcular el límite de la función simplificada
        limite = sympy.limit(funcion_simplificada, variable, punto)

        # Verificar casos especiales
        if limite == sympy.oo or limite == -sympy.oo:
            proceso.append("El límite tiende a infinito.")
            return "∞", proceso
        elif limite == sympy.zoo:
            proceso.append("El límite es indefinido.")
            return "Indefinido", proceso

        # Convertir a valor decimal solo si es necesario
        if isinstance(limite, sympy.Expr) and not limite.is_number:
            limite_valor = limite.evalf()
        else:
            limite_valor = limite

        proceso.append(f"Resultado del límite: {formatear_fraccion(limite_valor)}")
        return limite_valor, proceso



    except Exception as e:
        proceso.append(f"Error al calcular el límite: {e}")
        return "Indefinido", proceso

# Función para formatear fracciones visualmente
def formatear_fraccion(expresion):
    
    if isinstance(expresion, sympy.Rational) or isinstance(expresion, sympy.Mul):
        
        numerador, denominador = expresion.as_numer_denom()
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
    
    return str(expresion)

# Función para graficar la función
def graficar_funcion(funcion, variable, punto):
    
    plt.clf()  
    plt.close()
    
    # Convertir la función a una forma que pueda ser evaluada numéricamente
    f_lambdified = sympy.lambdify(variable, funcion, 'numpy')
    
    # Dos graficas para evitar unión en el centro
    x_vals_neg = np.linspace(punto - 10, punto - 0.1, 100, endpoint=True, dtype=float)
    x_vals_pos = np.linspace(punto + 0.1, punto + 10, 100, endpoint=True, dtype=float)
    
    # Generar los valores de y para los dos rangos de x (antes y después de la discontinuidad)
    y_vals_neg = []
    y_vals_pos = []
    
    # Para valores de x a la izquierda del punto de discontinuidad
    for val in x_vals_neg:
        try:
            y = f_lambdified(val)
            if np.abs(y) > 1e10:  # Umbral para valores muy grandes
                y_vals_neg.append(np.nan)
            else:
                y_vals_neg.append(y)
        except ZeroDivisionError:
            y_vals_neg.append(np.nan)  # Si hay una división por cero, asignar NaN
    
    # Para valores de x a la derecha del punto de discontinuidad
    for val in x_vals_pos:
        try:
            y = f_lambdified(val)
            if np.abs(y) > 1e10:  # Umbral para valores muy grandes
                y_vals_pos.append(np.nan)
            else:
                y_vals_pos.append(y)
        except ZeroDivisionError:
            y_vals_pos.append(np.nan)  # Si hay una división por cero, asignar NaN
    
    # Crear la gráfica: dos segmentos separados 
    plt.plot(x_vals_neg, y_vals_neg, color='b')  
    plt.plot(x_vals_pos, y_vals_pos, color='b', label=str(funcion))  
    
    # Limite en la gráfica
    try:
        limite = sympy.limit(funcion, x, punto)
        limite_valor = float(sympy.N(limite))
        plt.scatter([punto], [limite_valor], color='red', zorder=5, label=f'Limite en x={punto} ({limite_valor})', marker='o', facecolors='white', edgecolors='red', s=100)
        
    except ZeroDivisionError:
        pass  # Si ocurre una división por cero al marcar el límite, no mostrar el punto
    except Exception as e:
        print(f"Error al calcular el límite para graficar: {e}")
    
    # Etiquetas y título
    plt.axvline(x=punto, color='gray', linestyle='--', label=f'x={punto}')
    plt.axhline(0, color='black',linewidth=1)
    plt.axvline(0, color='black',linewidth=1)
    plt.title(f'Gráfica del límite cuando x tiende a {punto}')
    plt.gcf().canvas.manager.set_window_title("Gráfico Generado por el CIPAS")  # Cambia el título de la ventana
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para obtener los datos de entrada
def obtenerDatos(entrada_funcion, entrada_punto):
    
    # Se encierra el proceso de obtención de datos para manejar errores
    try:
        # Lee los datos de entrada y los prepara para su uso
        funcion_str = entrada_funcion.get()
        funcion_str = funcion_str.replace("^", "**")
        funcion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_str) # Reemplazar la multiplicación implícita, como '3x' por '3*x'

        # Diccionario con funciones trigonométricas reconocidas
        trig_funcs = {
            'seno': 'sin',
            'coseno': 'cos',
            'tangente': 'tan',
            'sec': 'sec',
            'cosec': 'csc',
            'cot': 'cot',
            'raiz': 'sqrt',
            'logaritmo': 'log',
            'e^': 'exp'
        }

        # Reemplazar funciones en español o comunes
        for esp, sym in trig_funcs.items():
            funcion_str = funcion_str.replace(esp, sym)

        # Convertir a función simbólica con las funciones reconocidas por sympy
        funcion = sympy.sympify(funcion_str, locals={'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
                                                    'sec': sympy.sec, 'csc': sympy.csc, 'cot': sympy.cot,
                                                    'exp': sympy.exp, 'log': sympy.log, 'sqrt': sympy.sqrt})

        # Validación de punto
        try:
            punto = float(entrada_punto.get())
        except ValueError:
            messagebox.showerror("Error", "El valor de x debe ser un número.")
            return None, None  # Retornar None si hay error

        punto = round(punto, 2)
        return funcion, punto

    except Exception as e:
        messagebox.showerror("Error", "Hubo un error al obtener los datos. Verifique la sintaxis de la función.")
        return None, None

# Función que se ejecuta con el botón "Calcular Límite"
def obtener_limite(entrada_funcion, entrada_punto, resultado_text):
    
    # Se encierra el proceso de solución para manejar errores
    try:
        funcion, punto = obtenerDatos(entrada_funcion, entrada_punto)  
        if funcion is None or punto is None:
            return
        limite, proceso = calcular_limite(funcion, x, punto)
        
        # Limpiar el Text widget antes de mostrar el nuevo proceso
        resultado_text.config(state=NORMAL)
        resultado_text.delete(1.0, END) 
        
        # Mostrar el resultado del límite y el proceso paso a paso
        resultado_text.insert(INSERT, f"Proceso de solución:\n")
        for paso in proceso:
            resultado_text.insert(INSERT, f"{paso}\n")
        
        resultado_text.config(state=DISABLED)
        
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error al calcular el límite o graficar la función.\n" + str(e) + "\nVerifique la función ingresada y el punto.")

# Función que se ejecuta con el botón "Graficar Límite"
def dibujar_limite(entrada_funcion, entrada_punto):
    
    # Se encierra el proceso de graficación para manejar errores
    try:
        funcion, punto = obtenerDatos(entrada_funcion, entrada_punto)  
        if funcion is None or punto is None:
            return
        graficar_funcion(funcion, x, punto)  
    except Exception as e:
        messagebox.showerror("Error", "Hubo un error al calcular el límite o graficar la función.\n" + str(e) + "\nVerifique la función ingresada y el punto.")

# Configuración de la ventana principal
root = Tk()
root.title("Programa Limites del mejor CIPAS")
root.geometry("505x500")
root.resizable(False, False) 

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
resultado_text.insert(INSERT, "Presentado por:\n\nDaniel Esguerra: 085453642024\nMichael Martinez: 085453942024\nJhonatan Rojas: 085450022024\nJavier Zapata: 085453922024\n\nFunciones que puede necesitar:\nseno\ncoseno\ntangente\nraiz")
resultado_text.config(state=DISABLED)  # Deshabilitar edición

# Ejecutar la interfaz gráfica
root.mainloop()
