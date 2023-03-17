array2D = []

filename = 'basic_strategy.txt'

with open(filename, 'r') as f:
    for line in f.readlines():
        array2D.append(line.split(','))

for row in array2D:
    for e in row:
        print(e)

print(array2D[9][8])
