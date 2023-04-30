from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from tkinter import colorchooser
import datetime

from translate import Translator

from threading import Timer
import time
import re

import PyPDF2
import pandas as pd
import clipboard
from bs4 import BeautifulSoup
import speech_recognition as sr

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


#Taustavärin vaihto, väri saadaan dropvarista eli pudotusvalikosta
def changeColor(event=''):
    textbox.config(bg=dropVar.get())


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


def redoTxt(event=''):
    textbox.edit_redo()


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

#html tiedoston luku, josta on ensin poistettu kaikki html-tägit
def readhtml():
    file = filedialog.askopenfilename()
    f = open(file)
    cleantext = BeautifulSoup(f,'lxml').text
    textbox.insert(INSERT,cleantext,END)


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

#Tässä määritellään uusi ikkuna ja sen komponentit
def csvrows():
        
        f = filedialog.askopenfilename()
        csvRowWindow = Toplevel(root)
        fromlbl = Label(csvRowWindow,text='start from:')
        fromRow = Entry(csvRowWindow,width=5)
        tolbl = Label(csvRowWindow,text='To:')
        toRow = Entry(csvRowWindow,width=5)
       
        fromlbl.pack()
        fromRow.pack()
        tolbl.pack()
        toRow.pack()
       
       
       #tässä määritellään csv-tiedoston lukemiseen tarvittavat asiat
        def readcsv():
            startrow = int(Entry.get(fromRow))
            stoprow = int(Entry.get(toRow))
            df = pd.read_csv(f,delim_whitespace = True)
            textbox.insert(INSERT,df.iloc[startrow:stoprow],END)
        csvReadBtn=Button(csvRowWindow,text='Read',command=readcsv)
        csvReadBtn.pack()

        


def excelrows():
    f = filedialog.askopenfilename()
    #uuden ikkunan, tekstien ja painikkeen määrittely
    rowWindow = Toplevel(root)
    rowlbl = Label(rowWindow,text='How many rows? ')
    rows = Entry(rowWindow,width=5)
    sheetlbl = Label(rowWindow, text='Type sheet name')
    sheet = Entry(rowWindow)
    AllVar = IntVar()
    ReadAll = Checkbutton(rowWindow,text='Read all', variable=AllVar,background='slate gray')
        
    
    
    rowlbl.pack()
    rows.pack()
    sheetlbl.pack()
    sheet.pack()
    ReadAll.pack()
    
    #huomaa että tämä funktio on määritelty excelrows funktion sisällä, muuten se ei toimi
    #toivotulla tavalla
    def readexcel():
        
        rowsInput =int(Entry.get(rows))
        sheetInput = (Entry.get(sheet))
        dfText = pd.read_excel(f,sheet_name=sheetInput,nrows=rowsInput)
        textbox.insert(INSERT,dfText,END)
    #uuden ikkunan painike määritellään funktion ulkopuolella
    readBtn = Button(rowWindow,text='Read',command=readexcel)
    readBtn.pack()  

def fontSizer():
    fontWindow = Toplevel(root)
    fontlbl = Label(fontWindow,text='Set size')
    fsize = Entry(fontWindow,width=5)
    selVar = IntVar()
    selOnly = Checkbutton(fontWindow,text='Selected only',variable=selVar)
    #FontSize = int(Entry.get(fsize))
    #textbox.config(font='Courier',size=FontSize)
    fontlbl.pack()
    selOnly.pack()
    fsize.pack()
    def setSize():
        #tallennetaan muuttujiin menuvalikon boolean muuttjien true/false arvo
        cour = fontCourier.get()
        aria = fontArial.get()
        taho = fontTahoma.get()
        syst = fontSystem.get()
        FontSize = int(Entry.get(fsize))
        useCourier = Font(family='Courier',size=FontSize)
        useArial = Font(family='Arial',size=FontSize)
        useTahoma = Font(family='Tahoma',size=FontSize)
        useSystem = Font(family='System',size=FontSize)

        #jos cour ja checkbox on valittu 
        if cour and selVar.get()==1 and textbox.tag_ranges('sel'):
            #lisätään thisOne niminen tagi, johon tallennetaan maalatusta merkkijonon kohdasta
            #merkit ensimmäisesti viimeiseen
            textbox.tag_add('thisOne',SEL_FIRST,SEL_LAST)
            #tagin sisällä oleva merkkijono saa fontikseen muuttujan sisältämän fontin
            textbox.tag_configure('thisOne',font=useCourier)
        else:
            textbox.config(font=useCourier)
            fontWindow.destroy()

         
        if aria and selVar.get()==1 and textbox.tag_ranges('sel'):
             textbox.tag_add('thisOne',SEL_FIRST,SEL_LAST)
            
             textbox.tag_configure('thisOne',font=useArial)
        else:

            textbox.config(font=useArial)
            fontWindow.destroy()

        if taho and selVar.get()==1 and textbox.tag_ranges('sel'):

            textbox.tag_add('thisOne',SEL_FIRST,SEL_LAST)
            textbox.tag_configure('thisOne',font=useTahoma)
    
        else:
            textbox.config(font=useTahoma)
            fontWindow.destroy()

        if syst and selVar.get()==1 and textbox.tag_ranges('sel'):
            textbox.tag_add('thisOne',SEL_FIRST,SEL_LAST)
            textbox.tag_configure('thisOne',font=useSystem)

        else:

            textbox.config(font=useSystem)
            fontWindow.destroy()
            

    
    setBtn = Button(fontWindow,text='Set size',command=setSize)
    setBtn.pack()

def copytext():
    if copyAll.get() == 1:
        #kopioidaan koko textboxin sisältö
        copytxt = textbox.get('1.0',END)
        clipboard.copy(copytxt)
    elif copySelected.get() == 1:
    
        #kopioidaan vain maalattu osa tekstistä
        copytxt = textbox.selection_get()
        clipboard.copy(copytxt)

#tämä laskee merkkien määrän
def countChars():
    content = textbox.get('1.0',END)
    #ei lasketa välilyöntejä, ainaostaan merkit.splitillä jokainen merkki lisätään taulukkoon
    #omaksi alkiokseen
    total = sum(map(len,(content.split())))
    #muutetaan tulos merkkijonoksi, että voidaan yhdistää total length teksti ja tulos widgetissä
    totalstr = str(total)
    #lisätään tulos charlbl label-widgettiin
    charlbl.config(text='Total length: '+totalstr)

def speechToTxt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        audioText = r.listen(source,timeout=5)
        #audiodata täytyy tallentaa tavalliseen muuttujaan, että se näkyy
        #tekstinä textbox widgetissä. timeoutilla määritellään mikrofonin kuunteluaika
        audioStr=r.recognize_google(audioText)
        
        textbox.insert(INSERT,audioStr,END)

#funktio ottaa parametrina enterin painalluksen ja tulostaa textboxin kulloisenkin
#indeksinumeron (rivinumeron) rowbox widgettiin.
def getrow(event):
    index = textbox.index(INSERT)
    row = index.split(".")[0]
    rowbox.insert(INSERT,row,END)
    rowbox.insert(INSERT,'\n',END)
    #rivilaskenta toteutetaan aina enterin painalluksesta, kutsutaan samassa funktiossa
    #myös merkkienlasku funtiota, jolloin päivittyy samalla kertaa rivimäärä ja merkkimäärä.
    countChars()
    
def keyRel(event2):
    countChars()

def DoTranslate():
    selected = textbox.selection_get()
    toLng = (Entry.get(setLng))
    translator= Translator(to_lang=toLng)
    translation = translator.translate(selected)
    #indeksinumerointi alkaa numerosta 1.0 = ensimmäinen rivi
    index = textbox.index(INSERT)
    
    #rivinvaihdon jälkeen row eli rivinumero kasvaa
    textbox.insert(index,'\n',END)
    #seuraava käännös näytetään aina uudella rivillä, koska row muuttuja arvo kasvaa
    #jokaisen rivinvaihdon jälkeen.
    textbox.insert(index,translation,END)
 
        


root = Tk()
root.geometry('700x700')
# määritellään käyttöliittymäikkunan kooksi 250 * 250 pikseliä.
root.configure(background='slate gray')  # määritellään ikkuna-komponentin taustaväri.
root.title('SimpleNote')  # annetaan ikkunassa näkyvä otsikko.

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)
frame5 = Frame(root)
frame6 = Frame(root)
frame7 = Frame(root)
frame8 = Frame(root)

frame2.configure(background='slate gray')
frame4.configure(background='slate gray')
frame5.configure(background='slate gray')
frame6.configure(background='slate gray')
frame7.configure(background='slate gray')
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
funcmenu.add_command(label='Count characters', command=countChars,accelerator='Ctrl+M')

#boolean muuttujan menubarin checkboxeille
fontCourier = BooleanVar()
fontArial = BooleanVar()
fontTahoma = BooleanVar()
fontSystem = BooleanVar()
menubar.add_cascade(label='Fonts', menu=fontmenu)
fontmenu.add_checkbutton(label='Courier', variable=fontCourier, command=fontSizer)
fontmenu.add_checkbutton(label='Arial', variable=fontArial, command=fontSizer)
fontmenu.add_checkbutton(label='Tahoma', variable=fontTahoma, command=fontSizer)
fontmenu.add_checkbutton(label='System', variable = fontSystem, command=fontSizer)
fontmenu.add_command(label='Choose font color', command=colorTxt)

menubar.add_cascade(label='Align text', menu=formmenu)
formmenu.add_command(label='Center', command=txtCenter)
formmenu.add_command(label='Right', command=txtRight)
formmenu.add_command(label='Left', command=txtLeft)

menubar.add_cascade(label='Read PDF/xlsx',menu=pdfmenu)
pdfmenu.add_command(label='Open PDF',command=readpdf)
pdfmenu.add_command(label='Open Excel',command=excelrows)
pdfmenu.add_command(label='Open CSV',command=csvrows)
pdfmenu.add_command(label='Open HTML',command=readhtml)


root.bind('<Control-o>', loadTxt)
root.bind('<Control-s>', saveTxt)
root.bind('<Control-t>', timeAndDate)
root.bind('<Control-u>', underline)
root.bind('<Control-h>',checkText)
root.bind('<Control-l>',changeColor)
#root.bind('<Control-m>',countChars)
root.bind('<Control-r>',redoTxt)


# tallennetaan muuttujaan georgia fontti koossa 11, jota käytetään ohjelman otsikossa.
titlefont = Font(family='Segoe Print', size=11)
lblfont = Font(family='Segoe Print', size=8)


scrollbar = Scrollbar(frame1)  # luodaan rullauspalkki ohjelmaan.
scrollbar.pack(side=RIGHT, fill=Y)  # asemoidaan rullauspalkki oikealle, fill komennolla kerrotaan rullaussuunta.

# luodaan label-komennolla tekstikomponentti. text-komennolla annetaan komponentissa näkyvä teksti, background
# komennolla komponentin taustaväri ja font komennolla käytettävä fontti.
name = Label(root, text='Simple Notepad', background='white smoke', font=titlefont, relief='solid')
#3 firstletter ja firstleter.trace + textvariable tarvitaan että voidaan automaattisesti
#muuttaa search entryyn syötetyn merkkijonon ensimmäinen kirjain isoksi kirjaimeksi.
charlbl = Label(root,background='slate gray')
firstLetter = StringVar()
search = Entry(frame4,textvariable=firstLetter)
firstLetter.trace('w',firstUpper)
# luodaan tekstikentta niminen tekstilaatikko, width ja height komennoilla määritellään sen koko.
textbox = Text(frame1, width=80, height=20, yscrollcommand=scrollbar.set, undo=True)
#bindataan enter ja getrow funktio
textbox.bind("<Return>",getrow)
#bindaus, aina kun jokin näppäin kutsutaan keyRel funkiota, keyrel kutsuu
#puolestaan countchar funktiota, joka laskee merkkien.tällä bindauksella
#saadaan realiaikainen merkkimäärän päivitys
textbox.bind('<KeyRelease>',keyRel)
#textbox.bind('<Return>',countChars)
rowbox = Text(frame1,width=2,background='gray')
scrollbar.config(command=textbox.yview)
downpart = Label(frame2, background='slate gray')
timedBtn = Button(frame2, text=' Enable timed save', command=timedSave)
distimedBtn = Button(frame2, text='Disable timed save', command=disTimedSave)
srcBtn=Button(frame4,text='Search',command=findTxt)
speechBtn = Button(frame7, text='speech to text',command=speechToTxt)

copyAll = IntVar()
all = Checkbutton(frame5,text='Copy all text', variable=copyAll,background='slate gray')


copySelected = IntVar()
selected = Checkbutton(frame5,text='Copy selected text', variable=copySelected,background='slate gray')
copyBtn = Button(frame5,text='Copy', command=copytext)


seconds = [5, 10, 15, 20, 25, 30]
setTime = ttk.Combobox(frame2, width=5, values=seconds)
setTimeOut = ttk.Combobox(frame7, width=5, values=seconds)

languages = ['german','spanish','french','chinese']
setLng = ttk.Combobox(frame8,width=5,values=languages)
setLng.current(1)
translateBtn = Button (frame8,text='Translate',command=DoTranslate)
#pudotusvalikko taustavärin vaihtoon
dropVar = StringVar()
dropVar.set('Select background color and  ctrl+l')
drop = OptionMenu(frame6,dropVar,'blue','red','white','gray')
#lbl = Label(root,text='').pack()

name.pack(pady=4, padx=4)


frame3.pack()
canvas.pack()
# kuvan lisäys/koon määroitys canvas-komponenttiin
canvas.create_image(8, 8, anchor=NW, image=noteImage)

frame4.pack()
frame8.pack()
frame1.pack()

# setFont.pack()

search.pack(pady=5,padx=5,side=LEFT)
srcBtn.pack(pady=5,padx=5,side=RIGHT)

setLng.pack(side=LEFT)
translateBtn.pack(side=RIGHT)
frame5.pack(side=LEFT)
all.pack()
selected.pack()
copyBtn.pack(side=LEFT,pady=2, padx=2)

rowbox.pack(side=LEFT,pady=1,padx=1)
textbox.pack(pady=2, padx=2)
charlbl.pack()
frame7.pack()
setTimeOut.pack(side=LEFT,pady=2, padx=2)
speechBtn.pack(side=RIGHT)

frame2.pack(side=RIGHT)
timedBtn.pack()
setTime.pack()
distimedBtn.pack()
frame6.pack()
drop.pack(side=BOTTOM,pady=4, padx=4)
downpart.pack()

mainloop()

