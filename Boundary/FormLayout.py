from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Control.ControlDocument import ControlDokumen
from Control.ControlPreprocessing import ControlPreprocessing
from Control.ControlSummarization import ControlSummarization
from Control.ControlAccuration1 import ControlAccuration

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

        mainFrame = Frame(frame, bd=0)
        mainFrame.pack(fill=BOTH, side=TOP)
        self.label = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.label.pack(side=TOP, fill=X, pady=10)

        frameBody = Frame(mainFrame, bd='5')
        frameBody.pack(fill=X, side=TOP)
        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.pack(padx=5, side=LEFT)
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
        # self.tree.bind("<Double-1>", self.OnDoubleClick)

        # self.buttonReset = Button(frame, text="Reset", command=self.resetDocument)
        # self.buttonReset.pack(side=LEFT, padx=10)
        self.buttonRingkas = Button(frame, text="Lakukan Peringkasan ->", state=DISABLED,
                                    command=lambda: self.showFrame(frameName="FormSummarization"))
        self.buttonRingkas.pack(side=RIGHT, padx=10)

        self.dokumen = []

    # def OnDoubleClick(self, event):
    #     # item = self.tree.identify('item',event.x,event.y)
    #     infoBerita = self.tree.item(self.tree.selection())['values']
    #     # isiBerita = self.controlDokumen.getBerita(infoBerita[0])
    #
    #     # judulIsi = self.dokumen[infoBerita[0]]
    #     print()

    # def resetDocument(self):
    #     self.entryBrowse.delete(0, END)
    #     self.controlDokumen.resetDocument()
    #     self.tree.delete(*self.tree.get_children())

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
            self.buttonRingkas['state'] = 'normal'

    def showFrame(self, frameName):
        self.controller.showFrame(frameName)


class FormSummarization(Frame):
    def __init__(self, parent, controller):
        self.controlPreprocessing = ControlPreprocessing()
        self.controlSummarization = ControlSummarization()
        self.resultSummary = []

        Frame.__init__(self, parent)
        self.controller = controller
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)
        mainFrame.pack(fill=BOTH, side=TOP)
        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.judul.pack(side=TOP, fill=X, pady=10)

        frameBody = Frame(mainFrame, bd='5')
        frameBody.pack(fill=X, side=TOP)

        self.buttonPreprocessing = Button(frameBody, text="Preprocessing", command=self.doPreprocessing)
        self.buttonPreprocessing.pack(side=LEFT, padx=10)

        self.labelExecution = Label(frameBody, text="", anchor=W, font=("Times New Roman", 13))
        self.labelExecution.pack(side=LEFT, fill=X, padx=10)

        frameText = Frame(mainFrame, padx=25)
        frameText.pack(fill=BOTH, expand=YES)

        self.label = Label(frameText, text="Hasil Ringkasan:", anchor=W, font=("Times New Roman", 15))
        self.label.pack(side=TOP, fill=X)

        # frameText = Frame(mainFrame, padx=25)
        # frameText.pack(fill=BOTH, expand=YES)

        self.textFile = Text(frameText, wrap=WORD, height=11, width=90, font=("Times New Roman", 12), spacing1=1)
        self.textFile.pack(fill=X, side=LEFT)
        self.sbVer = Scrollbar(frameText, orient=VERTICAL, command=self.textFile.yview)
        self.sbVer.pack(side=LEFT, fill=Y)
        self.textFile.config(yscrollcommand=self.sbVer.set)

        frameBottom = Frame(mainFrame, bd=5)
        frameBottom.pack(fill=X, side=BOTTOM)

        self.buttonKembali = Button(mainFrame, text="Kembali", command=lambda: controller.showFrame("FormMainMenu"))
        self.buttonKembali.pack(side=LEFT, pady=10, padx=10)
        self.buttonRingasBerita = Button(mainFrame, state=DISABLED, text="Ringkas", command=self.doSummarization)
        self.buttonRingasBerita.pack(side=LEFT, padx=270, pady=10)
        self.buttonHitungAkurasi = Button(mainFrame, text="Hitung Akurasi->", state=DISABLED,
                                          command=lambda: self.showFrame("FormAccuration"))
        self.buttonHitungAkurasi.pack(side=RIGHT, padx=10, pady=10)
        # self.sentencesDocument = []
        # self.preprocessingResult = []
        # self.progress = Label(frameBottom)
        # self.progress.pack(side=BOTTOM)

    def doPreprocessing(self):
        start = time.time()
        formMainMenu = self.controller.getFrame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        self.controlPreprocessing.doPreprocessing(dokumen)
        self.buttonRingasBerita['state'] = 'normal'
        end = time.time()
        self.labelExecution['text'] = ("Preprocessing Time: %.3f second" % (end - start))

    def doSummarization(self):
        start = time.time()
        sentencesDocument = self.controlPreprocessing.getSentencesDocument()
        preprocessingResult = self.controlPreprocessing.getResultPreprocessing()
        self.controlSummarization.doSummarization(preprocessingResult, sentencesDocument)
        self.resultSummary = self.controlSummarization.getResultSummary()
        end = time.time()
        # print("execution time: " + str(end - start))
        self.labelExecution['text'] = ("Summarization Time: %.3f second" % (end - start))
        for sentence in self.resultSummary:
            self.textFile.insert(INSERT, sentence + " ")
        self.buttonHitungAkurasi['state'] = 'normal'

    def getSumber(self):
        formMainMenu = self.controller.getFrame("FormMainMenu")
        dokumen = formMainMenu.dokumen
        for d in dokumen.values():
            print(d)

    def showFrame(self, frameName):
        self.controller.showFrame(frameName)


class FormAccuration(Frame):
    def __init__(self, parent, controller):
        self.controlDokumen = ControlDokumen()
        self.controlAccuration = ControlAccuration()
        Frame.__init__(self, parent)
        self.controller = controller
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)
        mainFrame.pack(fill=BOTH, side=TOP)

        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", font=("Times New Roman", 18))
        self.judul.pack(side=TOP, fill=X, pady=10)

        frameBody = Frame(mainFrame, bd='5')
        frameBody.pack(fill=X, side=TOP)
        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.pack(padx=5, side=LEFT)
        self.buttonBrowse = Button(frameBody, text='Browse', command=self.browseAccuration)
        self.buttonBrowse.pack(side=LEFT, padx=10)

        self.tree = ttk.Treeview(mainFrame, height=8)
        self.tree['column'] = ("sumber","Rouge-1.Recall","Rouge-1.Precision","Rouge-1.F-measure")
        self.tree.column("#0", width=30, anchor=CENTER)
        self.tree.column("sumber", width=90, anchor=W)
        self.tree.column("Rouge-1.Recall", width=115, anchor=CENTER)
        self.tree.column("Rouge-1.Precision", width=115, anchor=CENTER)
        self.tree.column("Rouge-1.F-measure", width=115, anchor=CENTER)

        self.tree.heading('#0', text="No.")
        self.tree.heading('sumber', text="Sumber")
        self.tree.heading('Rouge-1.Recall', text="ROUGE-1.Recall")
        self.tree.heading('Rouge-1.Precision', text="Rouge-1.Precision")
        self.tree.heading('Rouge-1.F-measure', text="Rouge-1.F-measure")
        self.tree.pack(side=LEFT, padx=10, pady=3)

        self.tree2 = ttk.Treeview(mainFrame, height=4)
        self.tree2['column'] = ("rogue", "akurasi")
        self.tree2.column("#0", width=40)
        self.tree2.column("rogue", width=140, anchor=W)
        self.tree2.column("akurasi", width=100, anchor=CENTER)
        self.tree2.heading('#0', text="No.")
        self.tree2.heading('rogue', text="ROUGE-1multi")
        self.tree2.heading('akurasi', text="Nilai")
        self.tree2.pack(side=TOP, padx=10, pady=3)

        frameBottom = Frame(mainFrame, bd=5)
        frameBottom.pack(fill=X, side=BOTTOM)

        self.buttonCountAccuration = Button(frame, text='Hitung Akurasi', command=self.countAccuration)
        self.buttonCountAccuration.pack(side=TOP, pady=10)

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
            i = 1
            for file in self.listFile:
                dokumen = file.split('-')
                self.tree.insert('', 'end', text=str(i), values=(dokumen[0]))
                i += 1
        self.controlDokumen.saveSummaries(folderPath)

    def countAccuration(self):
        listSumber = ['CNN', 'Detik', 'Kompas', 'Liputan6', 'Merdeka', 'Okezone', 'Tempo']
        summaries = self.controlDokumen.getSummaries()
        formSummarization = self.controller.getFrame("FormSummarization")
        listSentence = formSummarization.resultSummary
        self.controlAccuration.doAccuration(summaries, listSentence)
        accuration = self.controlAccuration.getResultAccuration()

        self.tree.delete(*self.tree.get_children())
        z = 1
        for list in sorted(listSumber):
            self.tree.insert('', END, text=str(z), values=(list,round(accuration[list][0],3),
                                                           round(accuration[list][1],3),round(accuration[list][2], 3)))
            z += 1
        Rouge1multi = {}
        Rouge1multi['recall'] = sum(acc for acc in [accuration[i][0] for i in accuration])/len(accuration)
        Rouge1multi['precision'] = sum(acc for acc in [accuration[i][1] for i in accuration])/len(accuration)
        Rouge1multi['fmeasure'] = sum(acc for acc in [accuration[i][2] for i in accuration])/len(accuration)

        self.tree2.insert('', END, text=str('1'), values=('Rouge-1multi Recall',round(Rouge1multi['recall'], 3)))
        self.tree2.insert('', END, text=str(2), values=('Rouge-1multi Precision',round(Rouge1multi['precision'], 3)))
        self.tree2.insert('', END, text=str('3'), values=('Rouge-1multi F-measure',round(Rouge1multi['fmeasure'], 3)))


    # if __name__ == "__main__":
    #     start = time.time()
    #     # not recommended
    #     # folderPath = 'D:/Dropbox/TA/Berita/Antasari'  # lebih bagus 0.65
    #     # folderPath = 'D:/Dropbox/TA/Berita/Timnas Tahan Imbang Vietnam (ok)'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Donald Trump Tolak Gaji'
    #     # folderPath = 'D:/Dropbox/TA/Berita/8. Gol Offside Man. City' #not recommended
    #     # folderPath = 'D:/Dropbox/TA/Berita/Nokia Android' zzz
    #     # folderPath = 'D:/Dropbox/TA/Berita/3. 76 WN China dirazia'
    #     # folderPath = 'D:/Dropbox/TA/Berita/6. New Yaris Heykers (no)'
    #
    #     # folderPath = 'D:/Dropbox/TA/Berita/Irman Gusman Divonis 4,5 Tahun Penjara'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Pesawat PM Israel Hindari Wilayah RI'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Gempa 5,2 SR Guncang Bali'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Whatsapp Hentikan Dukungan Untuk Blackberry & Nokia'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Hugo Barra Tinggalkan Xiaomi'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Xiaomi Memperkenalkan Mi Notebook Air'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Harga Pertamax, Pertalite, dan Dexlite Naik'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Leicester City Pecat Manajer Ranieri'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Ahmad Dhani Dilaporkan ke Polisi'
    #     # folderPath = 'D:/Dropbox/TA/Berita/Abduh Curhat Ke Jokowi'
    #
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Irman Gusman'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Pesawat PM Israel Hindari Wilayah RI'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Gempa 5,2 SR'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Whatsapp'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Hugo'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Mi Notebook Air'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Pertalite'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Manajer Liecester'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Ahmad Dhani'
    #     # folderPath2 = 'D:/Dropbox/TA/Ringkasan/Ringkasan Abduh'
    #
    #     folderPath =  []
    #     folderPath2 = []
    #     folderPath.append('D:/Dropbox/TA/Berita/Irman Gusman Divonis 4,5 Tahun Penjara')
    #     folderPath.append('D:/Dropbox/TA/Berita/Pesawat PM Israel Hindari Wilayah RI')
    #     folderPath.append('D:/Dropbox/TA/Berita/Gempa 5,2 SR Guncang Bali')
    #     folderPath.append('D:/Dropbox/TA/Berita/Whatsapp Hentikan Dukungan Untuk Blackberry & Nokia')
    #     folderPath.append('D:/Dropbox/TA/Berita/Hugo Barra Tinggalkan Xiaomi')
    #     folderPath.append('D:/Dropbox/TA/Berita/Xiaomi Memperkenalkan Mi Notebook Air')
    #     folderPath.append('D:/Dropbox/TA/Berita/Harga Pertamax, Pertalite, dan Dexlite Naik')
    #     folderPath.append('D:/Dropbox/TA/Berita/Leicester City Pecat Manajer Ranieri')
    #     folderPath.append('D:/Dropbox/TA/Berita/Ahmad Dhani Dilaporkan ke Polisi')
    #     folderPath.append('D:/Dropbox/TA/Berita/Abduh Curhat Ke Jokowi')
    #
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Irman Gusman')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Pesawat PM Israel Hindari Wilayah RI')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Gempa 5,2 SR')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Whatsapp')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Hugo')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Mi Notebook Air')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Pertalite')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Manajer Liecester')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Ahmad Dhani')
    #     folderPath2.append('D:/Dropbox/TA/Ringkasan/Ringkasan Abduh')
    #
    #     for i in range(len(folderPath)):
    #         # print(folderPath[i])
    #         # print(folderPath2[i])
    #         controlDokumen = ControlDokumen()
    #         controlPreprocessing = ControlPreprocessing()
    #         controlSummarization = ControlSummarization()
    #         controlAccuration = ControlAccuration()
    #
    #         controlDokumen.saveDocument(folderPath[i])
    #         dokumen = controlDokumen.getDocument()
    #
    #         controlPreprocessing.doPreprocessing(dokumen)
    #         sentencesDocument = controlPreprocessing.getSentencesDocument()
    #         preprocessingResult = controlPreprocessing.getResultPreprocessing()
    #
    #         controlSummarization.doSummarization(preprocessingResult, sentencesDocument)
    #         listSentence = controlSummarization.getResultSummary()
    #
    #         # for sentence in listSentence:
    #         #     print(sentence)
    #         # print()
    #
    #         controlDokumen.saveSummaries(folderPath2[i])
    #         summaries = controlDokumen.getSummaries()
    #         controlAccuration.doAccuration(summaries, listSentence)
    #         accuration = controlAccuration.getResultAccuration()
    #
    #         for key in sorted(accuration):
    #             # print("%s %s" %(key,accuration[key]))
    #             print("%s, %s" %(key,accuration[key]))
    #         print()
    #
    #         # listRouge={}
    #         # listRouge['ROUGE-1.Min'] = min(acc for acc in accuration.values())
    #         # listRouge['ROUGE-1.Avg'] = sum(acc for acc in accuration.values()) / len(accuration)
    #         # listRouge['ROUGE-1.Max'] = max(acc for acc in accuration.values())
    #
    #         # for list in listRouge.items():
    #         #     print(list)
    #
    #         # print("MIN: %s" % (listRouge['ROUGE-1.Min']))
    #         # print("MIN: %s" % (listRouge['ROUGE-1.Min']))
    #         # print("MAX: %s" % (listRouge['ROUGE-1.Max']))
    #
    # end = time.time()
    # print("Execution time:" + str(end - start))


if __name__ == "__main__":
    app = ControlForm(title="Program Tugas Akhir")
    app.mainloop()
