from csv import reader
from math import sqrt

import matplotlib.pyplot as plt
import pandas as pd


# Cargar el dataset csv
def cargar_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Convertir filas (string) => (float)
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())  # Elimina whitespaces de c/u column


# Captura las clases y las etiqueta con un int
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    # Diccionario con las valores de clases
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup


# Encuentra el valor maximo y minimo de columna
# [[minColum1,MaxColum1],[minColum2,MaxColum2],..]
def dataset_minmax(dataset):
    minmax = list()
    for i in range(len(dataset[0])):
        col_values = [row[i] for row in dataset]
        value_min = min(col_values)
        value_max = max(col_values)
        minmax.append([value_min, value_max])
    return minmax


# Calcular la distancias euclidiano entre 2 vectores
def distancia_euclidiana(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


# Localizar los vecinos similares
def get_vecinos(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = distancia_euclidiana(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors


# Realizar predicciones de vecinos similares
def predecir_clasificacion(train, test_row, num_neighbors):
    neighbors = get_vecinos(train, test_row, num_neighbors)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


# Obtener Path dataset
filename = 'datasets/dataset01.txt'
dataset = cargar_csv(filename)

for i in range(len(dataset[0]) - 1):
    str_column_to_float(dataset, i)

# Identidica las clases del dataset con un entero
str_column_to_int(dataset, len(dataset[0]) - 1)

# Numero de vecinos a considerar
knn = 5

# Puntos de prueba
row = [5.01212, -10.12125]
row2 = [8, 125, 96, 0, 0, 0.0, 0.232, 54]

# Realizar la prediccion pasando un punto
label = predecir_clasificacion(dataset, row, knn)
print('Punto Evaluado=%s, Clasificacion: %s' % (row, label))

# print("dataset_minmax")
# minMax = dataset_minmax(dataset)
# print("%s \n" %(minMax))

# Dibujar con matplotlib
plt.plot(row[0], row[1], marker="o", color="red")
plt.plot(row[1], row[0], marker="o", color="red")
plt.show()
# Utilizando Pandas
dataset_path = 'datasets/dataset03.txt'
input = pd.read_csv(dataset_path, sep=";")

print(len(input))
##<<<<TERMINAR<<<<
##Agregar cond de separadores csv
## Filtrar cabecera
## Grafica de puntos
## Particionar el dataset 0.75 train ; 0.25 test
