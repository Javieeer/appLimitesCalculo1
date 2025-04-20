# Calculadora de Límites con Visualización Gráfica

Este es un proyecto educativo desarrollado en Python que permite calcular el límite de una función cuando la variable tiende a un valor determinado. Además, muestra paso a paso el proceso y genera una gráfica que ayuda a visualizar el comportamiento de la función alrededor del punto de interés.

## 📌 Características

- Interfaz gráfica intuitiva construida con `Tkinter`.
- Soporte para funciones algebraicas y trigonométricas (`sen`, `cos`, `tan`, `log`, etc.).
- Visualización gráfica del límite usando `Matplotlib`.
- Muestra el paso a paso del proceso de cálculo, incluyendo la factorización simbólica.
- Manejo de errores y validación de entrada del usuario.

## ⚙️ Tecnologías utilizadas

- Python 3.x
- [SymPy](https://www.sympy.org) – Cálculo simbólico.
- [NumPy](https://numpy.org) – Evaluación numérica.
- [Matplotlib](https://matplotlib.org) – Gráficos.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – Interfaz gráfica.

## 🚀 Instalación

1. Clona el repositorio o descarga el archivo principal:

```bash
git clone https://github.com/tu_usuario/limites-cipas.git
cd limites-cipas
```
2. Instala las dependencias necesarias:
```
pip install sympy numpy matplotlib
```
3. Ejecuta el archivo principal:
```
python main.py
```
Nota: Tambien puedes ejecutarlo directamente con el ejecutable. Encuentralo en la carpeta dist como ".exe"

## ✍️ Cómo usarlo
1. Ingresa la función en el campo correspondiente. Ejemplos válidos:

- 3x^2 + 2x - 1
- seno(x)/x
- (x^2 - 1)/(x - 1)

2. Escribe el valor al que tiende x, por ejemplo 1.

3. Haz clic en Calcular Límite para obtener el resultado y el proceso paso a paso.

4. Haz clic en Graficar Límite para visualizar el comportamiento de la función cerca del punto.

## 👨‍💻 Autores
Proyecto desarrollado por estudiantes del programa de Ingeniería en Sistemas:

- Daniel Esguerra – 085453642024
- Michael Martínez – 085453942024
- Jhonatan Rojas – 085450022024
- Javier Zapata – 085453922024

## 📜 Licencia
Este proyecto es de uso académico. Puedes modificarlo y compartirlo con fines educativos. 🚀