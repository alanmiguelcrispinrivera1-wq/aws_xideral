# Tarea 3 - Explicar los siguientes métodos y sus respectivos conceptos de estadística 

Las siguientes métricas estadísticas se calculan utilizando el método describe() en la librería Pandas. El método 
describe() nos sirve para generar un resumen estadístico rápido y completo de las columnas numéricas de un DataFrame.
Es importante saber que también se pueden obtener las métricas estadísticas de forma individual utilizando sus 
respectivos métodos que veremos a continuación.

## Método `count()`
count nos indica cuantos valores existen en el conjunto de datos. Podemos decir que mide la frecuencia absoluta 
contando el número total de observaciones o elementos válidos. Matemáticamente, representa el **tamaño de la muestra n**
(n es el conjunto de datos) 

## Método `mean()`
mean es la **media aritmética**, también conocida como **promedio aritmético**. Se calcula sumando todos los valores numéricos y 
dividiendo el resultado entre el número total de elementos (n). Podemos interpretar la media como el punto de 
equilibrio de los datos

## Método `std()`
std es la **desviación estándar**. Lo que hace es cuantificar la dispersión o variabilidad de los datos en torno a su
medida. Se calcula como la raíz cuadrada de la varianza muestral (dividiendo entre n-1 para grados de libertad en
Pandas/NumPy). Su objetivo es medir que tan dispersos están los datos alrededor de la media. Es importante saber que 
los valores altos indican mayor dispersión, mientras que valores cercanos a cero indican que los datos están concentrados 
cerca del promedio.

## Método `min()`
min es el **valor mínimo absoluto** dentro de la serie numérica, que define el límite inferior del conjunto de datos.
Básicamente, es la función que busca el menor valor observado.

# Cuantiles
Los cuantiles son **medidas de posición** no central que dividen un conjunto de datos ordenados de menor a mayor en partes
iguales. Hay distintos tipos de cuantiles:

+ Cuartiles: Dividen el conjunto en 4 partes iguales.
+ Quintiles: Dividen el conjunto en 5 partes iguales.
+ Deciles: Dividen el conjunto en 10 partes iguales. 
+ Percentiles: Dividen el conjunto en 100 partes iguales.

## 25% - Primer cuartil (Q1)
Es un valor estadístico perteneciente a los cuartiles que divide un conjunto de datos ordenados de menor a mayor en 
cuatro partes iguales, de modo que el 25% (primer cuartil) de los datos se encuentran por debajo de este valor y el
75% por encima.

## 50% - Mediana - Segundo cuartil (Q2)
Es la **mediana**, o sea, el valor central que divide el conjunto de datos ordenados de menor a mayor en dos 
mitades exactas (50% por debajo y 50% por encima). Si el número de elementos es par, se obtiene promediando los dos
valores centrales.

## 75% - Tercer cuartil (Q3)
Es un valor estadístico perteneciente a los cuartiles que divide un conjunto de datos ordenados de menor a mayor en 
cuatro partes iguales, de modo que el 75% (tercer cuartil) de los datos se encuentran por debajo de este valor y el
25% por encima.

## Método `max()`
max es el valor máximo absoluto dentro de la serie numérica, que define el límite superior del conjunto de datos.
Básicamente, es la función que busca el mayor valor observado.
