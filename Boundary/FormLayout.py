from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Control.ControlDocument import ControlDokumen
from Control.ControlPreprocessing import ControlPreprocessing
from Control.ControlSummarization import ControlSummarization

import os


class ControlForm(Tk):
    def __init__(self, title, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.centerWindow()
        self.title(title)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)

        self.frames = {}
        for F in (FormMainMenu, FormSummarization, FormAccuration):
            pageName = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pageName="FormMainMenu")

    def get_frame(self, pageName):
        return self.frames[pageName]

    def show_frame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def centerWindow(self):
        w = 813
        h = 500
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))


class FormMainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controlDokumen = ControlDokumen()
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)  # , bg = 'blue'
        mainFrame.pack(fill=BOTH, side=TOP)  # both = X and Y

        self.label = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.label.pack(side=TOP, fill=X, pady=10)

        frameBody = Frame(mainFrame, bd='5')  # , bg='pink'
        frameBody.pack(fill=X, side=TOP)

        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.pack(side=LEFT)

        self.buttonBrowse = Button(frameBody, text='Browse', command=self.openFile)
        self.buttonBrowse.pack(side=LEFT, padx=10)

        self.tree = ttk.Treeview(frame)
        self.tree['column'] = ("sumber", "judul")
        self.tree.column("#0", width=40)
        self.tree.column("sumber", width=250, anchor=W)
        self.tree.column("judul", width=500)
        self.tree.heading('#0', text="No.")
        self.tree.heading('sumber', text="Sumber")
        self.tree.heading('judul', text="Judul")
        self.tree.pack(padx=10, pady=15)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        self.buttonReset = Button(frame, text="Reset", command=self.resetDocument)
        self.buttonReset.pack(side=LEFT, padx=10)
        self.buttonRingkas = Button(frame, text="Ringkas", command=lambda: controller.show_frame("FormSummarization"))
        self.buttonRingkas.pack(side= TOP,padx=50)
        self.dokumen = {}

    # belum di pakai
    def OnDoubleClick(self, event):
        # item = self.tree.identify('item',event.x,event.y)
        infoBerita = self.tree.item(self.tree.selection())['values']
        # isiBerita = self.controlDokumen.getBerita(infoBerita[0])

        # judulIsi = self.dokumen[infoBerita[0]]
        print()

    def resetDocument(self):
        self.entryBrowse.delete(0, END)
        self.controlDokumen.resetDocument()
        self.tree.delete(*self.tree.get_children())

    def openFile(self):
        checkItem = self.tree.get_children()
        if checkItem != '()':
            for row in checkItem:
                self.tree.delete(row)

        folderPath = filedialog.askdirectory()
        if folderPath:
            self.entryBrowse.insert(0, (folderPath))
            self.listFile = os.listdir(folderPath)
            i = 1
            for file in self.listFile:
                dokumen = file.split('-')
                self.tree.insert('', 'end', text=str(i), values=(dokumen[0], dokumen[1][:-4]))
                i += 1
            self.controlDokumen.saveDocument(folderPath)
            self.dokumen = self.controlDokumen.getDocument()


class FormSummarization(Frame):
    def __init__(self, parent, controller):
        self.controlPreprocessing = ControlPreprocessing()
        self.controlSummarization = ControlSummarization()
        Frame.__init__(self, parent)
        self.controller = controller
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)  # , bg = 'blue'
        mainFrame.pack(fill=BOTH, side=TOP)  # both = X and Y

        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.judul.pack(side=TOP, fill=X, pady=10)

        frameBody = Frame(mainFrame, bd='5')
        frameBody.pack(fill=X, side=TOP)

        self.label = Label(frameBody, text="Hasil Ringkasan:", anchor=W, font=("Times New Roman", 15))
        self.label.pack(side=TOP, fill=X)

        frameText = Frame(mainFrame, padx=25)
        frameText.pack(fill=BOTH, expand=YES)

        self.textFile = Text(frameText, height=18, width=90)
        self.textFile.pack(fill=X, side=LEFT)
        self.sbVer = Scrollbar(frameText, orient=VERTICAL, command=self.textFile.yview)
        self.sbVer.pack(side=LEFT, fill=Y)
        self.textFile.config(yscrollcommand=self.sbVer.set)

        frameBottom = Frame(mainFrame, bd=5)
        frameBottom.pack(fill=X, side=BOTTOM)

        self.buttonKembali = Button(frameBottom, text="Kembali", command=lambda: controller.show_frame("FormMainMenu"))
        self.buttonKembali.pack(side=LEFT, pady=10)
        self.buttonTest = Button(frameBottom, text="Test", command=self.doSummarization)
        self.buttonTest.pack(side=LEFT, pady=10)
        self.buttonHitungAkurasi = Button(frameBottom, text="Hitung Akurasi",
                                          command=lambda: controller.show_frame("FormAccuration"))
        self.buttonHitungAkurasi.pack(side=RIGHT, pady=10)

    def doSummarization(self):
        formMainMenu = self.controller.get_frame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        self.controlPreprocessing.doPreprocessing(dokumen)
        sentencesDocument = self.controlPreprocessing.getSentencesDocument()
        preprocessingResult = self.controlPreprocessing.getPreprocessing()
        self.controlSummarization.doSummarization(preprocessingResult, sentencesDocument)

    def getSumber(self):
        formMainMenu = self.controller.get_frame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        for d in dokumen.values():
            print(d)


class FormAccuration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)  # , bg = 'blue'
        mainFrame.pack(fill=BOTH, side=TOP)  # both = X and Y

        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.judul.pack(side=TOP, fill=X, pady=10)


if __name__ == "__main__":
    app = ControlForm(title="Program Tugas Akhir")
    app.mainloop()
