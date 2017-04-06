# from numpy import *
#
#
# x=[[1,0],[0,1],[1,1],[2,3]]
#
# print(x)
# matrix = array(x)
# print(matrix)
#
# U, s, Vh = linalg.svd(matrix, full_matrices=False)
# print (U)
# print()
# print (s)
# print ()
# print (Vh)

from tkinter import *
master = Tk()

def var_states():
   print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))

var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)
Button(master, text='Show', command=var_states).grid(row=4, sticky=W, pady=4)
# if(var1==True):
#     print(True)
mainloop()