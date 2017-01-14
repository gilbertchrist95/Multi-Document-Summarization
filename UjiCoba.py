# import tkinter as tk
# from UjiCoba2 import StartPage
# from UjiCoba3 import PageOne
#
#
# titleFont = ("Helvetica",18,'bold')
#
# class SampleApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self,*args,**kwargs)
#
#         container = tk.Frame(self)
#         container.pack(side='top',fill='both', expand=True)
#         # container.grid_rowconfigure(0,weight=1)
#         # container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#         for F in (StartPage,PageOne):
#             # page_name = F.__name__
#             frame = F(container, self)
#             self.frames[F]=frame
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame(StartPage)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()

# import time, sys
#
# # update_progress() : Displays or updates a console progress bar
# ## Accepts a float between 0 and 1. Any int will be converted to a float.
# ## A value under 0 represents a 'halt'.
# ## A value at 1 or bigger represents 100%
# def update_progress(progress):
#     barLength = 10 # Modify this to change the length of the progress bar
#     status = ""
#     if isinstance(progress, int):
#         progress = float(progress)
#     if not isinstance(progress, float):
#         progress = 0
#         status = "error: progress var must be float\r\n"
#     if progress < 0:
#         progress = 0
#         status = "Halt...\r\n"
#     if progress >= 1:
#         progress = 1
#         status = "Done...\r\n"
#     block = int(round(barLength*progress))
#     text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
#     sys.stdout.write(text)
#     sys.stdout.flush()
#
#
# # update_progress test script
#
# update_progress("hello")
# time.sleep(1)
#
#
# update_progress(3)
# time.sleep(1)
#
#
# update_progress([23])
# time.sleep(1)
#
# update_progress(-10)
# time.sleep(2)
#
# update_progress(10)
# time.sleep(2)
#
# for i in range(100):
#     time.sleep(0.1)
#     update_progress(i/100.0)
#
# time.sleep(10)

import tkinter as tk
import tkinter.ttk as ttk

# class App:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.tree = ttk.Treeview()
#         self.tree.pack()
#         for i in range(10):
#             self.tree.insert("", "end", text="Item %s" % i)
#         self.tree.bind("<Double-1>", self.OnDoubleClick)
#         self.root.mainloop()
#
#     def OnDoubleClick(self, event):
#         item = self.tree.identify('item',event.x,event.y)
#         print("you clicked on", self.tree.item(item,"text"))
#
# if __name__ == "__main__":
#     app = App()

#
# listoflists = []
# a_list = []
# for i in range(0,10):
#     a_list.append(i)
#     if len(a_list)>3:
#         a_list.remove(a_list[0])
#         listoflists.append((list(a_list), a_list[0]))
# print (listoflists)

# list = [['gilbert','adalah','nama','saya'],	['lyncia','adalah','adik','saya','perempuan'],['gerend','adalah','adik','saya','laki-laki.']]
# dict= {}
# dict['cnn'] = list
# # dict['detik'] = list[1]
# # dict['okezone'] = list[2]
# cnn = dict['cnn']
# print(type(cnn))

# from tkinter import *
#
#
# def raise_frame(frame):
#     frame.tkraise()
#
# root = Tk()
#
# f1 = Frame(root)
# f2 = Frame(root)
# f3 = Frame(root)
# f4 = Frame(root)
#
# for frame in (f1, f2, f3, f4):
#     frame.grid(row=0, column=0, sticky='news')
#
# Button(f1, text='Go to frame 2', command=lambda:raise_frame(f2)).pack()
# Label(f1, text='FRAME 1').pack()
#
# Label(f2, text='FRAME 2').pack()
# Button(f2, text='Go to frame 3', command=lambda:raise_frame(f3)).pack()
#
# Label(f3, text='FRAME 3').pack(side='left')
# Button(f3, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')
#
# Label(f4, text='FRAME 4').pack()
# Button(f4, text='Goto to frame 1', command=lambda:raise_frame(f1)).pack()
#
# raise_frame(f1)
# root.mainloop()

# list = "indonesia adalah negeri kita. Jakarta adalah ibukotanya. Kita harus menjaganya! Mengapa masih ada orang rasis?"
import re

# pattern = re.compile("[.?!]")
# r = '.|!|?'
# list = re.split(pattern,list)
# list.pop()
# print(list)
# aa = list[1]
# aaa = aa.split()
# print(aaa)
# list = "indonesia adalah negeri kita. 12/12/202 \"Jakarta adalah ibukotanya\". Kita harus menjaganya! Mengapa masih ada orang rasis?"
# DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
#
#
# def tokenizing(text):
#     regexPattern = '|'.join(map(re.escape, DELIMETERS))
#     texts = re.split(regexPattern, text.lower())
#     return texts
#
#
test = ['acb', ' b']
a = ' '.join(test).split()
# test.clear()
print(a)

# def split(delimiters, string, maxsplit=0):
#     import re
#     regexPattern = '|'.join(map(re.escape, delimiters))
#     return re.split(regexPattern, string, maxsplit)
# delimiters = '.','!','?'
# regexPattern = '!'.join(map(re.escape,delimiters))
# print(re.split(regexPattern,list))

# arr = []
# arr.append([])
# arr[0].append('aa1')
# arr[0].append('aa2')
#
# print(type(arr))
# print(arr)

# import numpy as np
# x = np.empty((3,2),dtype=int)
# x[0,1]=1
# print(type(x))
#
# for i in range(5,3,-1):
# 	print("aa")


# matrix = [[0 for i in range(5)] for j in range(5)]
# print(type(matrix))
#
# for i in range(1,3):
# 	print(i)
#
# a = [['ini', 'adalah', 'indonesia'],['negeri', 'adalah', 'indonesia']]
# # b = ['indonesia', 'adalah', 'negeri']
# print(len(a))
# print(a[1])
# keys=  ['ini', 'adalah', 'indonesia','negeri']
# c =  {}
# i=0
#
# for j in a:
#     for token in j:
#         if token in c.keys():
#             c[token][i]+=1
#         else:
#             c[token]=[0]*3
#             c[token][i]=1
#     i+=1
#
#
# print(c)

# a={ 'a': [1,2], 'b': [2,3], 'c': [3,4] }
# list = [[k,v]for k,v in a.items()]
#
#
# zzz = [v[1] for v in a.values()]
# # for a in zzz:
# #     a.pop(0)
# print(zzz)
#
# A = [0,0,0]
# B=[1,2,3]
# C=[i+j for i,j in zip(B,A)]
# z=2
# C = [i/2 for i in (C)]
# print(C)
#
#
# theArray = [['a','b','c'],['d','e','f'],['g','h','i']]
# # print(list(map(list, zip(*theArray))))
# # list(itertools.zip_longest(*theArray))
# l = [[1,2,3],[4,5,6],[7,8,9]]
# # a = map(list,map(None,*l))
# print([[j[i] for j in l] for i in range(len(l))])
# # print(a.values())

a = ['gilbet','christopher']
print('gilbet' in a)

print(a.index('gilbet'))


from math import sqrt
a = [4,3]


def square(list):
    return sqrt(sum(map(lambda x: x ** 2, list)))

b=square(a)
print(b)

a = [x[:] for x in [[0] * 2] * 10]
print(a)

a = [2,3]
b = [4,6]
c = sum(map(lambda x,y:x*y, a, b))
print(c)