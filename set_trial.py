# set trial

X = {'a', 'b', 'c', 'd'}
Y = { x**2 for x in range(1,6)}
Z = X | Y

FOUND = {'MG1', 'MG2', 'W1'}

print(X)
print(Y)
print(Z)

print(FOUND | Z)




