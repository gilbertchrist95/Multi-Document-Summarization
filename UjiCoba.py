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

list = [['gilbert','adalah','nama','saya'],	['lyncia','adalah','adik','saya','perempuan'],['gerend','adalah','adik','saya','laki-laki.']]
dict= {}
dict['cnn'] = list
# dict['detik'] = list[1]
# dict['okezone'] = list[2]
cnn = dict['cnn']
print(type(cnn))