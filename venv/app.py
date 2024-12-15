#Utilizar Python para consumir APIs 
# pip install requests

import pandas as pd
import requests
import matplotlib.pyplot as plt

# El endPoint de todos los libros

url = "http://localhost:8000/books"

# Se realiza la petición por el método GET del endPoint de todos los libros
response = requests.get(url)
print(response.status_code) # se imprime el estado de http
# Se toma la respuesta de response
response_json = response.json()
#print(response_json)
df = pd.DataFrame(response_json)
print(df)

# Extraer los nombres de los talleres
listaTalleres = df['nombre_taller'].unique()
print(f"Lista de Talleres: {listaTalleres}")

# Resumen estadístico de las columnas numéricas:
print("Resumen Estadístico:")
print(df.describe())

# Contar el número de talleres
n_talleres = df['nombre_taller'].nunique()
print(f'Número de talleres: {n_talleres}')

# Funciones de Agrupación
# Por cantidad de cupos
cant_cupos = df.groupby('nombre_taller')['cupos'].sum().reset_index()
print("Cantidad total de cupos por taller:")
print(cant_cupos)

# Por promedio de duración
promedio_duracion = df.groupby('nombre_taller')['duracion(horas)'].mean().reset_index()
print("Duración promedio de los talleres:")
print(promedio_duracion)

# Ingresos potenciales por taller
df['ingreso_potencial'] = df['precio'] * df['cupos']
print("Ingresos potenciales por taller:")
print(df[['nombre_taller', 'ingreso_potencial']])

# Gráfico de barras: Precio de los talleres
plt.figure(figsize=(8, 5))
plt.bar(df['nombre_taller'], df['precio'], color='skyblue', alpha=0.8)
plt.title('Comparación de precios de los talleres')
plt.xlabel('Talleres')
plt.ylabel('Precio ($)')
plt.xticks(rotation=45)
plt.show()

# Gráfico de pastel: Proporción de cupos por taller
plt.figure(figsize=(7, 7))
plt.pie(df['cupos'], labels=df['nombre_taller'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribución de cupos por taller')
plt.show()

# Gráfico de dispersión: Relación entre duración y precio
plt.figure(figsize=(8, 5))
plt.scatter(df['duracion(horas)'], df['precio'], color='purple', alpha=0.7)
plt.title('Relación entre duración y precio de talleres')
plt.xlabel('Duración (horas)')
plt.ylabel('Precio ($)')
plt.grid(True)
plt.show()
