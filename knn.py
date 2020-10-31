"""""
CORE KNN
"""
import time
from csv import reader
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.colors import ListedColormap
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


# Actualmente NO USO
# Convertir filas (string) => (float)
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())  # Elimina whitespaces de c/u column


# Captura las clases y las etiqueta con un int
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    # print("***",type(class_values))
    # Diccionario con las valores de clases
    for i, value in enumerate(unique):
        lookup[value] = i
        # print(type(int(value)))
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
    distancia = 0.0
    for i in range(len(row1) - 1):
        distancia += (row1[i] - row2[i]) ** 2
    return sqrt(distancia)


# Localizar los vecinos similares
def get_vecinos(train, test_row, num_vecinos):
    distancia = list()
    for train_row in train:
        dist = distancia_euclidiana(test_row, train_row)
        distancia.append((train_row, dist))
    distancia.sort(key=lambda tup: tup[1])
    vecinos = list()
    for i in range(num_vecinos):
        vecinos.append(distancia[i][0])
        # Problema que %train dataset > k
    return vecinos


# Realizar predicciones de vecinos similares
def predecir_clasificacion(train, test_row, num_vecinos):
    vecinos = get_vecinos(train, test_row, num_vecinos)
    valores = [row[-1] for row in vecinos]
    prediccion = max(set(valores), key=valores.count)
    return prediccion


# Divide el dataset segun parametros seleccionado con porcentaje > 1
# preguntar al profe cual es el porc min
# Controlar qque porcentaje/100 * dataset>=10
def dividir_dataset(array, porcentaje):
    # resta = 1 if header else 0
    trainRange = round((len(array)) * (porcentaje / 100))
    train = []
    test = []
    for i in range(trainRange):
        train.append(array[i])
        # print(array[i])

    for i in range(trainRange, len(array)):
        test.append(array[i])
    return train, test


# Hasta 6 labels para clasificar en el plot
# Plotear
def dibujar_puntos(array, labels):
    # Set de colores
    colores = ["red", "blue", "green", "black", "yellow", "purple", "gray"]
    # Considero numero de clasificaciones posibles dentro del dataset <7
    # Recorto Array segun numero de labels en dataset, ya calculado
    colores = [colores[i] for i in range(len(labels))]
    # print(labels.keys())
    for i in range(len(array)):
        # Emocionante!
        # Verifico las labels de clasificacion
        # Obtengo el indice del label segun clasificacion [string]->int
        # Selecciono color segun posicion de la indice
        # La ultima es fila es label para plot
        color = colores[labels.get(array[i][len(array[i]) - 1])]
        plt.plot(array[i][0], array[i][1], marker="o", color=color)

    plt.show()


# Clasifica Test y devuelve resultados con metricas
def clasificar_datatest(train, test):
    acertados = 0
    resultados = dict()
    for k in range(1, 11):
        startTime = time.time()
        for i in range(len(test)):
            label = predecir_clasificacion(train, test[i], k)
            # print(type(label) == type(test[i][len(test[i])-1]))
            if (label == test[i][len(test[i]) - 1]):  # Verifico si hay acierto
                acertados += 1
            label = labels[label]
            print('Punto Evaluado=%s, Clasificacion: %s' % (test[i][0:len(test[i]) - 1], label))
        print("\nK:%s => Acertados: %s, Porcentaje: %s%s , Tiempo(seg): %s\n" % (
            k, acertados, round(acertados / len(test) * 100, 3), '%', time.time() - startTime))
        resultado = {"acertados": acertados, "porcentaje": acertados / len(test) * 100, "time": time.time() - startTime}
        resultados[k] = resultado
        acertados = 0
    # print("\n Diccionario", len(resultados))
    return resultados


# Estadisticas k=1..10
def medir_procesamiento(metrica):
    # Inicializaciones
    total = 0.0
    max = 0
    min = 1
    kmin = 0
    kmax = 0
    x = []
    y = []
    desv = 0.0
    # Busco los valores de los tiempos max y min
    for k in metrica:
        x.append(k)
        y.append(metrica[k]['time'])
        # print(metrica[k])
        total += metrica[k]['time']
        if (metrica[k]['time'] > max):
            max = metrica[k]['time']
            kmax = k
        if (metrica[k]['time'] < min):
            min = metrica[k]['time']
            kmin = k
    print("El K:%s (optimo seg):%s , K:%s (peor seg):%s  " % (kmin, metrica.get(kmin), kmax, metrica.get(kmax)))
    promedio = total / len(metrica)
    print("Promedio:", promedio)
    plt.plot(x, y)
    plt.xlabel("K")
    plt.ylabel("Procesamiento(seg)")
    # Calculo el desvio estandar
    for k in metrica:
        desv += (metrica[k]['time'] - promedio) ** 2
    desv = desv / len(metrica)
    print("Desvio estandar:", desv)
    # ploteo el promedio de tiempos encontrados
    plt.hlines(promedio, 1, 10, colors='red', linestyles="dashed", label="Media")
    plt.show()

#Verificar controles de carga archivo vacio o k con paramtros correctos
def control_entrada(input, k, porcentaje):
    # porcentaje = 75
    # k = 8
    if not input.empty:
        print("No vacio")
        train, test = dividir_dataset(input.to_numpy(), porcentaje)
        if len(train) >= k:
            if len(input) != len(train): #dataset >= train
                print("Clasificar")
                return True
            else:
                print("El dataset es todo Train, ingrese to a clasificar")
        else:
            print("Ingreso un k mayor a len Dataset")
            return False
    else:
        print("Dataset ingresado vacio")
        return False

#################################################################################################
# Cargar CSV
# Utilizando Pandas
def tratar_csv(dataset_path, sep, header):
    # dataset_path = 'datasets/dataset04.txt'
    # sep = ";"
    # header = 0 #0->con etiquetas, None -> sin etiquetas

    # Si no esta tildado el header se pone None
    # No esta considerando el primero en caso de no tener cabecera
    input = pd.read_csv(dataset_path, sep=sep, header=header)

    # Verifica si el archivo esta vacio

    flag = control_entrada(input, 8, 75)


    # Pasar de panda tabla a array

    array = input.to_numpy()
    array2 = np.array(input).tolist()
    # print(type(array))
    # print(array)
    # print(type(array2))
    # print(array2)
    if flag and type(array[0][len(array[0]) - 1]) == str:  # Verifico si la clase es String sino paso a int(mejora aciertos)
        print("String")
    else:
        print("Number")
        for i in range(len(array2)):
            a = int(array2[i][len(array2[i]) - 1])
            array2[i][len(array[i]) - 1] = a

    return array2
    # print(array2) #Transformador a Int

    # Identidica las clases del dataset con un entero
    #labels = str_column_to_int(array2, len(array2[0]) - 1)
    # print(labels)

    # Dividir dataset
    #train, test = dividir_dataset(array, 75)
    # ax=plt.gca()
    # for line in ax.lines:
    #     print(line.get_xdata)

    # Plotear dataset
    # dibujar_puntos(array, labels)

    # Clasificar datas
    # metrica = clasificar_datatest(train, test)

    # Estadisticas
    # medir_procesamiento(metrica)


    # Ver el tema de exportar funciones o meter en clases
