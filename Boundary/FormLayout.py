from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Control.ControlDocument import ControlDokumen
from Control.ControlPreprocessing import ControlPreprocessing
from Control.ControlSummarization import ControlSummarization
from Control.ControlAccuration import ControlAccuration

import os
import time


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
        self.showFrame(pageName="FormMainMenu")

    def getFrame(self, pageName):
        return self.frames[pageName]

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def centerWindow(self):
        w = 810
        h = 470
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))


class FormMainMenu(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.controlDokumen = ControlDokumen()

        Frame.__init__(self, parent)
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
        self.entryBrowse.pack(padx=5 ,side=LEFT)
        self.buttonBrowse = Button(frameBody, text='Browse', command=self.openFile)
        self.buttonBrowse.pack(side=LEFT, padx=10)

        self.tree = ttk.Treeview(frame, height=8)
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
        self.buttonRingkas = Button(frame, text="Ringkas", command=lambda: controller.showFrame("FormSummarization"))
        self.buttonRingkas.pack(side= TOP,padx=50)

        self.dokumen = []

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
        # print(folderPath)
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
        self.resultSummary = []

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

        self.textFile = Text(frameText, height=15, width=90)
        self.textFile.pack(fill=X, side=LEFT)
        self.sbVer = Scrollbar(frameText, orient=VERTICAL, command=self.textFile.yview)
        self.sbVer.pack(side=LEFT, fill=Y)
        self.textFile.config(yscrollcommand=self.sbVer.set)

        frameBottom = Frame(mainFrame, bd=5)
        frameBottom.pack(fill=X, side=BOTTOM)

        self.buttonKembali = Button(frameBottom, text="Kembali", command=lambda: controller.showFrame("FormMainMenu"))
        self.buttonKembali.pack(side=LEFT, pady=10)
        self.buttonTest = Button(frameBottom, text="Test", command=self.doSummarization)
        self.buttonTest.pack(side=LEFT, pady=10)
        self.buttonHitungAkurasi = Button(frameBottom, text="Hitung Akurasi",
                                          command=lambda: controller.showFrame("FormAccuration"))
        self.buttonHitungAkurasi.pack(side=RIGHT, pady=10)

    def doSummarization(self):
        formMainMenu = self.controller.getFrame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        self.controlPreprocessing.doPreprocessing(dokumen)
        sentencesDocument = self.controlPreprocessing.getSentencesDocument()
        preprocessingResult = self.controlPreprocessing.getPreprocessing()
        self.controlSummarization.doSummarization(preprocessingResult, sentencesDocument)
        self.resultSummary = controlSummarization.getResultSummary()

        for sentences in self.resultSummary:
            self.textFile.insert(INSERT,sentences+" ")

    def getSumber(self):
        formMainMenu = self.controller.getFrame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        for d in dokumen.values():
            print(d)


class FormAccuration(Frame):
    def __init__(self, parent, controller):
        self.controlDokumen = ControlDokumen()
        self.controlAccuration = ControlAccuration()
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

        frameBody = Frame(mainFrame, bd='5')  # , bg='pink'
        frameBody.pack(fill=X, side=TOP)
        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.pack(padx=5,side=LEFT)
        self.buttonBrowse = Button(frameBody, text='Browse', command=self.browseAccuration)
        self.buttonBrowse.pack(side=LEFT, padx=10)

        self.tree = ttk.Treeview(mainFrame,height = 8)
        self.tree['column'] = ("sumber", "judul")
        self.tree.column("#0", width=40)
        self.tree.column("sumber", width=140, anchor=W)
        self.tree.column("judul", width=140)
        self.tree.heading('#0', text="No.")
        self.tree.heading('sumber', text="Sumber")
        self.tree.heading('judul', text="Rouge-1")
        self.tree.pack(side=LEFT,padx=10, pady=10)

        self.tree2 = ttk.Treeview(mainFrame, height=4)
        self.tree2['column'] = ("rogue", "akurasi")
        self.tree2.column("#0", width=40)
        self.tree2.column("rogue", width=140, anchor=W)
        self.tree2.column("akurasi", width=140)
        self.tree2.heading('#0', text="No.")
        self.tree2.heading('rogue', text="Rogue-1")
        self.tree2.heading('akurasi', text="Akurasi")
        self.tree2.pack(side = TOP,padx=10, pady=10)

        frameBottom = Frame(mainFrame, bd=5)
        frameBottom.pack(fill=X, side=BOTTOM)

        self.buttonCountAccuration = Button(frame, text='Hitung Akurasi', command=self.countAccuration)
        self.buttonCountAccuration.pack(side=TOP)

        self.buttonKembali = Button(frame, text="Kembali", command=lambda: controller.showFrame("FormSummarization"))
        self.buttonKembali.pack(side=LEFT, pady=10, padx=10)

    def browseAccuration(self):
        checkItem = self.tree.get_children()
        if checkItem != '()':
            for row in checkItem:
                self.tree.delete(row)
        folderPath = filedialog.askdirectory()
        if folderPath:
            self.entryBrowse.insert(0, (folderPath))
            self.listFile = os.listdir(folderPath)
            i=1
            for file in self.listFile:
                dokumen = file.split('-')
                self.tree.insert('', 'end', text=str(i), values=(dokumen[0]))
                i += 1
        self.controlDokumen.saveSummarization(folderPath)

    def countAccuration(self):
        listSumber = ['CNN','Detik','Kompas','Liputan6','Merdeka','Okezone','Tempo']
        summaries = self.controlDokumen.getSummary()
        formSummarization = self.controller.getFrame("FormSummarization")
        listSentence = formSummarization.listSentence
        self.controlAccuration.doAccuration(summaries, listSentence)
        accuration = self.controlAccuration.getResultAccuration()
        self.tree.delete(*self.tree.get_children())
        z=1
        for list in listSumber:
            self.tree.insert('',END,text=str(z),values = (list,accuration[list]))
            z+=1


if __name__ == "__main__":
    controlDokumen = ControlDokumen()
    controlPreprocessing = ControlPreprocessing()
    controlSummarization = ControlSummarization()
    controlAccuration = ControlAccuration()

    # folderPath = 'D:/Dropbox/TA/Berita/1. Mi Notebook Air'
    # folderPath = 'D:/Dropbox/TA/Berita/9. Nokia Android'
    # folderPath = 'D:/Dropbox/TA/Berita/11. Timnas Tahan Imbang Vietnam (ok)'
    folderPath = 'D:/Dropbox/TA/Berita/Hugo Barra mundur dari Xiaomi (ok)'
    # folderPath = 'D:/Dropbox/TA/Berita/2. Whatsapp Stop Dokungan (not recommended)'

    controlDokumen.saveDocument(folderPath)
    dokumen = controlDokumen.getDocument()

    controlPreprocessing.doPreprocessing(dokumen)
    sentencesDocument = controlPreprocessing.getSentencesDocument()
    preprocessingResult = controlPreprocessing.getPreprocessing()

    controlSummarization.doSummarization(preprocessingResult,sentencesDocument)
    resultSummary = controlSummarization.getResultSummary()

    for summary in resultSummary:
        print(summary)

    folderPath2 = 'C:/Users/Gilbert/Desktop/Ringkasan/Hugo Barra Hengkang dari Xiaomi'
    controlDokumen.saveSummarization(folderPath2)
    summaries = controlDokumen.getSummary()
    controlAccuration.doAccuration(summaries,resultSummary)
    accuration = controlAccuration.getResultAccuration()
    print(accuration.items())

# if __name__ == "__main__":
#     # app = ControlForm(title="Program Tugas Akhir")
#     # app.mainloop()