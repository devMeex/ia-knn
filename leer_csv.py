from csv import reader

#Cargar archivo csv excluyendo filas vacias
def cargar_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset
#Convertir cada columna str -> float
def convertir_float(dataset, columna):
    for row in dataset:
        row[columna] = float(row[columna].strip())

filename = 'datasets/diabetes-test.csv'
dataset = cargar_csv(filename)
print('Loaded data file {0} with {1} rows and {2} columns').format(filename, len(dataset), len(dataset[10]))
print(dataset[0])

for i in range(len(dataset[0])):
    convertir_float(dataset,i)
print(dataset)

#Falta salta lineas comentadas