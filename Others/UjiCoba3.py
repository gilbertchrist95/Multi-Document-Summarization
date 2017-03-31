from numpy import *


x=[[1,0],[0,1],[1,1],[2,3]]

print(x)
matrix = array(x)
print(matrix)

U, s, Vh = linalg.svd(matrix, full_matrices=False)
print (U)
print()
print (s)
print ()
print (Vh)