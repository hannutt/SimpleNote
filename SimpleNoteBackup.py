from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from tkinter import colorchooser
import datetime

from threading import Timer
import time
import re

import PyPDF2
import pandas as pd

global currentFile
currentFile = False


# ajastettu tallennus olemassaolevaan tiedostoon.
def timedSave():
    if currentFile:
        tiedosto = open(currentFile,'a')  # Avataan tiedosto, jonka nimi on file-muuttujan syötetty tiedostonimi. w-kirjaimella
        # kerrotaan, että tallennus tehdään tekstimuodossa ja korvataan mahdollinen vanha sisältö.
        myText = textbox.get('1.0','end-1c')  # tallennetaan muuttujaan tekstikentän teksti ensimmäisestä kirjaimesta viimeiseen.
        tiedosto.write(myText)  # Kirjoitetaan teksti tiedostoon.
        sec = int(Entry.get(setTime))
        # globaali-muuttuja timerille, että sitä voidaan käyttää timerin pysäytykseen disTimedSave funktiossa
        global t
        # sec-muuttujaan on tallennettu setTime pudotusvalikosta valittu arvo. timedSave funktiota kutsutaan
        # aina sec-muuttujassa olevan sekuntimäärä välein.
        t = Timer(sec, timedSave)
        # ajastimen käynnistys
        t.start()
        tiedosto.close
        messagebox.showinfo('Saving', 'File saved!')
    else:
        messagebox.showinfo('Notice', 'Save text to file first!')


def disTimedSave():
    # pysäytetään ajastin
    t.cancel()

#parametrina otettaan event, eli tässä ohjelmassa bindattu ctrl+s. funktiota voi siis kutsua myös tuolla
#näppäinyhdistelmällä.
def saveTxt(event=''):  # Luodaan funktio, jolla tallennetaan kirjoitettu teksti.
    files = [('Text files', '*.txt')]

    file = filedialog.asksaveasfilename(filetypes=files,
                                        defaultextension=files)
    # file-muuttujaan tallennetaan tiedostolle annettava nimi. avaus ja tallentaminen
    # tapahtuu windows-käyttöjärjestelmän vakio-dialogeissa, joka on toteutettu
    # filedialog kirjastolla.

    tiedosto = open(file, 'w')  # Avataan tiedosto, jonka nimi on file-muuttujan syötetty tiedostonimi. w-kirjaimella
    # kerrotaan, että tallennus tehdään tekstimuodossa ja korvataan mahdollinen vanha sisältö.
    myText = textbox.get('1.0',
                         'end-1c')  # tallennetaan muuttujaan tekstikentän teksti ensimmäisestä kirjaimesta viimeiseen.
    tiedosto.write(myText)  # Kirjoitetaan teksti tiedostoon.

    messagebox.showinfo('Tallennus', 'Tiedosto on tallennettu!')  # näytetään ilmoitus erillisessä ikkunassa
    # kun tiedosto on tallennettu onnistuneesti.
    tiedosto.close  # suljetaan tiedosto.


# tallennus olemassaolevaan tiedostoon

def saveSame():
    global currentFile
    if currentFile:
        tiedosto = open(currentFile,
                        'w')  # Avataan tiedosto, jonka nimi on file-muuttujan syötetty tiedostonimi. w-kirjaimella
        # kerrotaan, että tallennus tehdään tekstimuodossa ja korvataan mahdollinen vanha sisältö.
        myText = textbox.get('1.0',
                             'end-1c')  # tallennetaan muuttujaan tekstikentän teksti ensimmäisestä kirjaimesta viimeiseen.
        tiedosto.write(myText)  # Kirjoitetaan teksti tiedostoon.

        messagebox.showinfo('Tallennus', 'Tiedosto on tallennettu!')  # näytetään ilmoitus erillisessä ikkunassa
        # kun tiedosto on tallennettu onnistuneesti.
        tiedosto.close  # suljetaan
    else:
        saveTxt()


def loadTxt(event=''):  # Luodaan funktio, jolla voidaan avata olemassaoleva tekstitiedosto.
    textbox.delete('1.0', END)
    haettava = filedialog.askopenfilename(
        initialdir='C:\\', )  # haettava muuttujaan tallennetaan avattavan tiedoston nimi,
    # initialdir komennolla asetetaan oletussijainniksi c-levy.

    if haettava:
        global currentFile
        currentFile = haettava

    tiedosto = open(haettava,
                    encoding='utf-8')  # avataan tiedosto ja käytetään siinä encoding komennolla utf-8 merkistökoodausta.
    textbox.insert('1.0', tiedosto.read())  # näytetään tiedoston teksti sisältö tekstikenttä laatikossa.
    tiedosto.close


def timeAndDate(event=''):
    timenow = datetime.datetime.now()
    result = timenow.strftime('%d/%m/%Y,%H:%M:%S')
    textbox.insert(INSERT, result, END)


# luodaan funktiot, joiden avulla voi vaihtaa fonttia. font komennolla määritellään, mitä fonttia käytetään.
def courier():
    textbox.config(font='Courier')


def arial():
    textbox.config(font='Arial')


def tahoma():
    textbox.config(font='Tahoma')


def system():
    textbox.config(font='System')


def clear():
    result = messagebox.askquestion('Delete all', 'Are you sure?')
    if result == 'yes':
        textbox.delete('1.0', END)


def txtCenter():
    # select = textbox.selection_get()
    textbox.tag_configure('center', justify='center')
    textbox.insert(1.0, " ")
    textbox.tag_add('center', '1.0', 'end')
    # textbox.tag_add('center',SEL_FIRST,SEL_LAST)


def txtRight():
    # select = textbox.selection_get()
    textbox.tag_configure('right', justify='right')
    textbox.insert(1.0, " ")
    textbox.tag_add('right', '1.0', 'end-1c')
    # textbox.tag_add('right',SEL_FIRST,SEL_LAST)


def txtLeft():
    # select = textbox.selection_get()
    textbox.tag_configure('left', justify='left')
    textbox.insert(1.0, " ")

    textbox.tag_add('left', '1.0', 'end-1c')


# textbox.tag_add('left',SEL_FIRST,SEL_LAST)


def underline(event=''):
    select = textbox.selection_get()
    textbox.tag_configure('1', underline='1')
    textbox.tag_add('1', SEL_FIRST, SEL_LAST, 'end')


def delUnderline():
    select = textbox.selection_get()
    textbox.tag_configure('0', underline='0')
    textbox.tag_add('0', SEL_FIRST, SEL_LAST, 'end')


def colorTxt():
    myColor = colorchooser.askcolor()[1]
    textbox.config(fg=myColor)


def redoTxt():
    textbox.edit_redo


#funktio tekstin hakuun
def findTxt():
    textbox.tag_remove('found','1.0',END)
    s = search.get()
    if s:
        idx='1.0'
        while 1:
            idx = textbox.search(s,idx,nocase=1,stopindex=END)
            if not idx:break
            lastidx = '%s+%dc' % (idx,len(s))
            textbox.tag_add('found',idx,lastidx)
            idx=lastidx
            textbox.tag_config('found',foreground='red')
        search.focus_set()

#funktio jolla muutetaan search entryyn syötetyn merkkijonon ensimmäinen kirjain
#isoksi kirjaimeksi
def firstUpper(*args):

    firstLetter.set(firstLetter.get().capitalize())


#automaattinen iso alkukirjain pisteen jälkeen
def checkText(event=''):
    content = textbox.get('1.0',END)
    #splitillä jaetaan lauseet osiin aina pisteen kohdalta.
    sentence = content.split('.')
    textbox.delete('1.0',END)
    for i in sentence:
        textbox.insert(INSERT,i.capitalize()+'. ',END)


def readpdf():
     f = filedialog.askopenfilename()
     pdfFileObj = open(f, 'rb')
     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # printing number of pages in pdf file
    #print('Number of pages: ',pdfReader.numPages)
     pageObj = pdfReader.getPage(0)
        # extracting text from page
     pdfText= pageObj.extractText()
     textbox.insert(INSERT,pdfText,END)
        # closing the pdf file object
     pdfFileObj.close()


def readexcel():

    dfText = pd.read_excel('sampledata.xlsx',sheet_name='Instructions',nrows=10)
    textbox.insert(INSERT,dfText,END)










root = Tk()
# määritellään käyttöliittymäikkunan kooksi 250 * 250 pikseliä.
root.configure(background='slate gray')  # määritellään ikkuna-komponentin taustaväri.
root.title('SimpleNote')  # annetaan ikkunassa näkyvä otsikko.

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)
frame2.configure(background='slate gray')
frame4.configure(background='slate gray')

canvas = Canvas(frame3, bg='white', height=55, width=55)

noteImage = PhotoImage(file='notes.png')

save = PhotoImage(file='NotepadSave.png')  # tuodaan png-kuvat ohjelmaan, joita käytetään kuvakkeina ohjelman pudotus
# valikossa.
finalsave = save.subsample(4, 4)

load = PhotoImage(file='NotepadOpen.png')
finalload = load.subsample(4, 4)

# luodaan alasvetovalikot toiminnoille ja fonteille.
menubar = Menu(root)
root.config(menu=menubar)
funcmenu = Menu(menubar)
fontmenu = Menu(menubar)
formmenu = Menu(menubar)
pdfmenu = Menu(menubar)

# Lisätään alasvetovalikkoihin toimintoja. command komennolla lisätään funktiot, jotka suoritetaan jos toiminto valitaan.
# image komennolla tuodaan kuvatiedosto tekstin yhteyteen, joka asetetaan compound komennolla tekstin oikealle puolelle.

menubar.add_cascade(label='Functions', menu=funcmenu)
funcmenu.add_command(label='Save', command=saveSame)
funcmenu.add_command(label='Save As', command=saveTxt, image=finalsave, compound=RIGHT, accelerator='Ctrl+S')

funcmenu.add_command(label='Load', command=loadTxt, image=finalload, compound=RIGHT, accelerator='Ctrl+O')
funcmenu.add_command(label='Insert time and date', command=timeAndDate, accelerator='Ctrl+T')
funcmenu.add_command(label='Underline text', command=underline, accelerator='Ctrl+U')
funcmenu.add_command(label='Remove underline', command=delUnderline)
funcmenu.add_command(label='Clear textbox', command=clear)
funcmenu.add_command(label='redo', command=redoTxt)

menubar.add_cascade(label='Fonts', menu=fontmenu)

fontmenu.add_command(label='Courier', command=courier)
fontmenu.add_command(label='Arial', command=arial)
fontmenu.add_command(label='Tahoma', command=tahoma)
fontmenu.add_command(label='System', command=system)
fontmenu.add_command(label='Choose font color', command=colorTxt)

menubar.add_cascade(label='Align text', menu=formmenu)
formmenu.add_command(label='Center', command=txtCenter)
formmenu.add_command(label='Right', command=txtRight)
formmenu.add_command(label='Left', command=txtLeft)

menubar.add_cascade(label='Read PDF/xlsx',menu=pdfmenu)
pdfmenu.add_command(label='Open PDF',command=readpdf)
pdfmenu.add_command(label='Open Excel',command=readexcel)

root.bind('<Control-o>', loadTxt)
root.bind('<Control-s>', saveTxt)
root.bind('<Control-t>', timeAndDate)
root.bind('<Control-u>', underline)
root.bind('<Control-h>',checkText)


# tallennetaan muuttujaan georgia fontti koossa 11, jota käytetään ohjelman otsikossa.
titlefont = Font(family='Segoe Print', size=11)

scrollbar = Scrollbar(frame1)  # luodaan rullauspalkki ohjelmaan.
scrollbar.pack(side=RIGHT, fill=Y)  # asemoidaan rullauspalkki oikealle, fill komennolla kerrotaan rullaussuunta.

# luodaan label-komennolla tekstikomponentti. text-komennolla annetaan komponentissa näkyvä teksti, background
# komennolla komponentin taustaväri ja font komennolla käytettävä fontti.
name = Label(root, text='Simple Notepad', background='white smoke', font=titlefont, relief='solid')
#3 firstletter ja firstleter.trace + textvariable tarvitaan että voidaan automaattisesti
#muuttaa search entryyn syötetyn merkkijonon ensimmäinen kirjain isoksi kirjaimeksi.
firstLetter = StringVar()
search = Entry(frame4,textvariable=firstLetter)
firstLetter.trace('w',firstUpper)
# luodaan tekstikentta niminen tekstilaatikko, width ja height komennoilla määritellään sen koko.
textbox = Text(frame1, width=100, height=20, yscrollcommand=scrollbar.set, undo=True)
scrollbar.config(command=textbox.yview)
downpart = Label(frame2, background='slate gray')
timedBtn = Button(frame2, text=' Enable timed save', command=timedSave)
distimedBtn = Button(frame2, text='Disable timed save', command=disTimedSave)
srcBtn=Button(frame4,text='Search',command=findTxt)

seconds = [5, 10, 15, 20, 25, 30]
setTime = ttk.Combobox(frame2, width=5, values=seconds)

name.pack(pady=4, padx=4)
frame3.pack()
canvas.pack()
# kuvan lisäys/koon määroitys canvas-komponenttiin
canvas.create_image(10, 10, anchor=NW, image=noteImage)
frame4.pack()
frame1.pack()
# setFont.pack()

search.pack(pady=5,padx=5,side=LEFT)
srcBtn.pack(pady=5,padx=5,side=RIGHT)
textbox.pack(pady=4, padx=4)
frame2.pack()
timedBtn.pack()
setTime.pack()
distimedBtn.pack()
downpart.pack()

mainloop()

