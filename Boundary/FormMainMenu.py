from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os


class FormMainMenu:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        # self.parent.protocol('WN_DELETE_WINDOW', self.exit)
        self.centerWindow()
        self.setComponent()

    def centerWindow(self):
        w = 800
        h = 500
        screenWidth = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def setComponent(self):
        frame = Frame(self.parent)  # bg='yellow'
        frame.pack(fill=X, side=TOP)

        mainFrame = Frame(frame, bd=0)  # , bg = 'blue'
        mainFrame.pack(fill=X, side=TOP)  # both = X and Y

        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", anchor=NW, font=("Times New Roman", 18))
        self.judul.pack(side=TOP, pady=15)

        frameBody = Frame(mainFrame, bd='5')  # , bg='pink'
        frameBody.pack(fill=X, side=TOP)

        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.grid(row=0, column=0, padx=5)

        self.buttonBrowse = Button(frameBody, text='Browse', command=self.openFile)
        self.buttonBrowse.grid(row=0, column=1)

        self.tree = ttk.Treeview(frame)
        self.tree['column'] = ("sumber", "judul")
        self.tree.column("#0", width=40)
        self.tree.column("sumber", width=250, anchor=W)
        self.tree.column("judul", width=500)
        self.tree.heading('#0', text="No.")
        self.tree.heading('sumber', text="Sumber")
        self.tree.heading('judul', text="Judul")
        self.tree.pack(padx=10, pady=15)

        self.buttonRingkas = Button(frame, text="Ringkas", command='')
        self.buttonRingkas.pack()

    def openFile(self):
        checkItem = self.tree.get_children()
        if checkItem != '()':
            for row in checkItem:
                self.tree.delete(row)

        folderPath = filedialog.askdirectory()
        self.entryBrowse.insert(0, (folderPath))
        self.listFile = os.listdir(folderPath)
        i = 1;
        for file in self.listFile:
            dokumen = file.split('-')
            self.tree.insert('', 'end', text=str(i), values=(dokumen[0], dokumen[1]))
            i += 1

if __name__ == '__main__':
    root = Tk()
    obj = FormMainMenu(root, title="Program Tugas Akhir")

    root.mainloop()
