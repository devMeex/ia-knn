"""""""""""""""""
--- CORE Algoritmo KNN ---
"""""""""""""""""
import time
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# Captura las clases y las etiqueta con un int
def str_column_to_int(dataset, columna):
    valores_clases = [row[columna] for row in dataset]
    unica = set(valores_clases)
    busqueda = dict()
    # Diccionario con las valores de clases
    for i, value in enumerate(unica):
        busqueda[value] = i
        # print(type(int(value)))
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[columna] = busqueda[row[columna]]
    return busqueda

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
def dividir_dataset(input, porcentaje):
    array = input.to_numpy()
    trainRange = round((len(array)) * (porcentaje / 100))
    train = []
    test = []
    for i in range(trainRange):
        train.append(array[i])

    for i in range(trainRange, len(array)):
        test.append(array[i])
    return train, test


# Hasta 6 labels para clasificar en el plot
# Plotear
def dibujar_puntos(input, labels):
    # Set de colores
    array=input.to_numpy()
    colores = ["red", "blue", "green", "black", "yellow", "purple", "gray"]
    # Considero numero de clasificaciones posibles dentro del dataset <7
    # Recorto Array segun numero de labels en dataset, ya calculado
    colores = [colores[i] for i in range(len(labels))]
    for i in range(len(array)):
        # Emocionante!
        # Verifico las labels de clasificacion
        # Obtengo el indice del label segun clasificacion [string]->int
        # Selecciono color segun posicion de la indice
        # La ultima es fila es label para plot
        color = colores[labels.get(array[i][len(array[i]) - 1])]
        plt.plot(array[i][0], array[i][1], marker="o", color=color)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Clasificación knn")
    plt.show()


#Grafica puntos clasificados y regiones asociadas para k
def plotear_grid(input,k, labels):
    train, test = dividir_dataset(input, 100)
    clasificados = []
    for i in range(len(input)):
        clasicado= predecir_clasificacion(train, train[i],k)
        clasificados.append(labels[clasicado])

    train = np.array(train)
    Arreglo = train[:, :2]
    h = .085 # Tamaño del peso en grid 03 default

    # Color de mapas: Backgrouds y points
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
    colores = ['#FF0000', '#00FF00', '#0000FF']

    #Verificar en labels el que tiene valor cero->rojo
    #el otro valor es azul
    x_min, x_max = Arreglo[:, 0].min() - 1, Arreglo[:, 0].max() + 1
    #print(x_min, x_max)
    y_min, y_max = Arreglo[:, 1].min() - 1, Arreglo[:, 1].max() + 1
    #print(y_min, y_max)
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    mezcla = np.c_[xx.ravel(), yy.ravel()]
    print(len(mezcla)) #Region a clasificar
    hora = time.time()
    x = []
    for j in range(len(mezcla)):
        clasificado = predecir_clasificacion(train, mezcla[j], k)
        clasificado = labels[clasificado]#Selecciona segun valor de etiqueta
        x.append(clasificado)
    x = np.array(x)

    print(time.time()-hora)#Finalizacion de Grafica
    x = x.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, x, cmap=cmap_light, shading='auto')
    plt.scatter(Arreglo[:, 0], Arreglo[:, 1], c=clasificados, cmap=cmap_bold)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Clasificación (k = %i, Distancia = 'Euclidiana')==> %s"
              % (k,labels))
    etiquetas = list(labels)
    red_patch = mpatches.Patch(color=colores[0], label=etiquetas[0])
    blue_patch = mpatches.Patch(color=colores[2], label=etiquetas[1])
    plt.legend(handles=[red_patch, blue_patch])
    #plt.grid()
    plt.show()


# Clasifica test y devuelve resultados con metricas k=1..10
def clasificar_datatest(train, test, labels):
    acertados = 0
    resultados = dict()
    if len(train) >= 11:
        max = 11
    else:
        max = len(train)

    for k in range(1, max):
        startTime = time.time()
        if(len(train)<k):
            return
        for i in range(len(test)):
            label = predecir_clasificacion(train, test[i], k)
            if (label == test[i][len(test[i]) - 1]):  # Verifico si hay acierto
                acertados += 1
            label = labels[label]
            print('Punto Evaluado=%s, Clasificacion: %s' % (test[i][0:len(test[i]) - 1], label))
        print("\nK:%s => Acertados: %s, Porcentaje: %s%s , Tiempo(seg): %s\n" % (
            k, acertados, round(acertados / len(test) * 100, 3), '%', time.time() - startTime))
        resultado = {"k": k, "acertados": acertados, "porcentaje": acertados / len(test) * 100, "time": time.time() - startTime}
        resultados[k] = resultado
        acertados = 0
    return resultados


# Estadisticas k=1..10
def medir_procesamiento(metrica):
    # Inicializaciones
    total = 0.0
    max = 0
    min = 100
    kmin = 0
    kmax = 0
    x = []
    y = []
    desv = 0.0
    # Busco los valores de los tiempos max y min
    for k in metrica:
        x.append(k)
        y.append(metrica[k]['porcentaje'])
        print(metrica[k])
        total += metrica[k]['porcentaje']
        if (metrica[k]['porcentaje'] > max):
            max = metrica[k]['porcentaje']
            kmax = k
        if (metrica[k]['porcentaje'] < min):
            min = metrica[k]['porcentaje']
            kmin = k
    print("El K:%s (Optimo):%s , K:%s (Peor):%s  " % (kmax, metrica.get(kmax),kmin, metrica.get(kmin)))
    promedio = total / len(metrica)
    print("Promedio de Aciertos de los K(%):", promedio)
    plt.plot(x, y)
    plt.xlabel("K")
    plt.ylabel("Aciertos(%)")
    # Calculo el desvio estandar
    for k in metrica:
        desv += (metrica[k]['porcentaje'] - promedio) ** 2
    desv = desv / len(metrica)
    print("Desvio estandar:", desv)
    # ploteo el promedio de tiempos encontrados
    plt.title("Porcentaje de aciertos")
    plt.hlines(promedio, 1, 10, colors='red', linestyles="dashed", label="Media")
    plt.legend()
    plt.show()
    return metrica.get(kmax), metrica.get(kmin), promedio, desv

#Verificar controles de carga archivo vacio o k con paramtros correctos
def control_entrada(input, k, porcentaje):
    # porcentaje = 75
    # k = 8
    if not input.empty:
        train, test = dividir_dataset(input, porcentaje)
        if len(train) >= k:
            if len(input) != len(train): #dataset >= train
                return True
            else:
                print("El dataset es no contiene datos de entrenamiento, ingrese to a clasificar")
                return True
        else:
            print("Ingreso un k mayor a len Dataset")
            return False, "Debe ingresar un porcentaje de entrenamiento y el valor de K seleccionado debe ser menor a la cantidad de registros que contiene el dataset"
    else:
        print("Dataset ingresado vacio")
        return False, "Dataset ingresado vacio"

# Verifico si la clase es String sino paso a int(mejora aciertos)
def clase_to_int(input):
    array = input.to_numpy()
    Datalist = np.array(input).tolist()
    if type(array[0][len(array[0]) - 1]) == str:
        print("String")
    else:
        print("Number")
        for i in range(len(Datalist)):
            a = int(Datalist[i][len(Datalist[i]) - 1])
            Datalist[i][len(array[i]) - 1] = a
    return Datalist

#Funcion de lectura del dataset c/ opciones de entrada y controles
#Opciones
def leer_dataset(path,k,porcentaje,sep, header):
    try:
        input = pd.read_csv(path, sep=sep, header=header)
        if control_entrada(input,k,porcentaje):
            Datalist = clase_to_int(input)
            labels = str_column_to_int(Datalist, len(Datalist[0]) - 1)
            return input, labels
        else:
            message = "Redefina las entradas"
            return message
    except Exception as e:
        print(e)#Muestro el error en la ventana

