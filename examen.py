# titulo = raw_input("Proporciona el titulo: ")
import math
import json
import random

a = random.randint(3,15)
b = random.randint(3,15)

x1 = []
x2 = []
dataSet = {}
dataSet['row1'] = []
dataSet['row2'] = []

for _ in range(b):
	x1.append(random.randint(0,3))
dataSet['row1'] = x1

for _ in range(a):
	x2.append(random.randint(0,3))
dataSet['row2'] = x2


def calcular_distancia ( a = 0, b = 0):
	return math.sqrt(a**2 + b**2)

# dataJson = json.dumps( dataSet )

# Almacenar en archivo mi json
with open('datajson', 'w') as file:
     json.dump(dataSet, file, indent=4)

# print(c)
print(dataSet['row1'])
print(dataSet['row1'][2])

tot = 0
for i in dataSet['row1']:
	tot += i
	print(i)
print("tot", tot)
tot = tot / float(len(dataSet['row1']))

print(len(dataSet['row1']))
print("tot", tot)
# print(calcular_distancia())
# print (calcular_distancia(2,b))