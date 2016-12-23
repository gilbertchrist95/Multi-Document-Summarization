from tkinter import *



class FormMainMenu:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        # self.parent.protocol('WN_DELETE_WINDOW', self.exit)
        # self.parent.resizeable(False,False)
        self.centerWindow()
        self.setComponent()

    def centerWindow(self):
        w = 800
        h = 600
        screenWidth = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def setComponent(self):
        frame = Frame(self.parent)
        frame.pack(fill=BOTH, expand=YES)

        mainFrame = Frame(frame, bd=0)
        mainFrame.pack(fill=BOTH, expand=YES)  # both = X and Y

        self.judul = Label(mainFrame,
                           text="Peringkasan Teks Multi-Dokumen dengan Menggunakan\nLatent Semantic Indexing dan\nSimilarity "
                                "Based Histogram Clustering", anchor=W, font=("Times New Roman", 18))
        self.judul.pack(side=TOP, pady=15)

        frameBody = Frame(mainFrame, bd=10, bg='pink')
        frameBody.pack(fill=BOTH, side=TOP, expand=YES)

        self.entryBrowse = Entry(frameBody, width=120)
        self.entryBrowse.grid(row=0, column=0, padx=5)

        self.buttonBrowse = Button(frameBody, text='Browse', command=self.parent.quit)
        self.buttonBrowse.grid(row=0, column=1)


if __name__ == '__main__':
    root = Tk()
    obj = FormMainMenu(root, title="Program Tugas Akhir")
    root.mainloop()
