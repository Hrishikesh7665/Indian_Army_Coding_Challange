#System Modules
#------------------
import os
import sys
import csv
import time
import ctypes
import signal
import sqlite3
import warnings
import pyperclip
import webbrowser
import PIL.Image
from tkinter import *
from PIL import ImageTk
from typing import Sized
import speech_recognition
from datetime import date, datetime
from tkinter import ttk, font, messagebox
from wikipedia import exceptions
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import  mixer
from threading import Thread

from MainModules.multiple_search_engines import MultipleSearchEngines, AllSearchEngines

#My Own Modules
#-------------------
try:
    from MainModules.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
    from MainModules.engines import search_engines_dict
    from MainModules import config
    from MainModules import webScrapping
except:
    print("Error To Importing The Additional Modules")
    sys.exit()

# Get Complete Path Of Given File Name
def resource_path(relative_path):
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    spriteFolderPath = os.path.join(CurrentPath, 'Resources')
    path = os.path.join(spriteFolderPath, relative_path)
    newPath = path.replace(os.sep, '/')
    return newPath

temp_directory = os.getenv("APPDATA")+"\\H_SearchEngine"

if (os.path.isdir(temp_directory)) == False:
    os.mkdir(temp_directory)

#Trying To Delete Previous Temp Files
def cleared_temp():
    files = [f for f in os.listdir(temp_directory) if os.path.isfile(os.path.join(temp_directory, f))]
    if len(files) > 0 :
        for i in range(len(files)):
            if files[i]!= "SearchHistory.db":
                os.remove(temp_directory+"\\"+str(files[i]))

temp_directory = os.getenv("APPDATA")+"\\H_SearchEngine\\"
Db_Path=temp_directory+"SearchHistory.db"

Background_Main = "#d7eff2"         #Main Background Color

MainWindow = Tk()                   #Main Tkinter Window

#Variables
Proxy_Load = False
CheckVar1 = IntVar(MainWindow)
CheckVar2 = IntVar(MainWindow)
CheckVar3 = IntVar(MainWindow)
CheckVar4 = IntVar(MainWindow)
CheckVar5 = IntVar(MainWindow)

Search_var=StringVar(MainWindow)

RadioNutton_VAR = IntVar(MainWindow)
Address_Entry_var = StringVar(MainWindow)
clicked = StringVar(MainWindow)
RadioNutton_VAR.set(1)
clicked.set("Yes")
Address_Entry_var.set("Hint:- protocol://ip:port ")

current_value = IntVar(MainWindow)
current_value.set(5)

#History Screen

His_frame = Frame(MainWindow,bg=Background_Main)


#Setting Screen

Setting_frame = Frame(MainWindow,bg=Background_Main)

#-----------------------------------------------------------------------------

def on_search_input_click(event):
    if Search_var.get() == 'Search The Web ':
        Search_Box.delete(0, "end") # delete all the text in the entry
        Search_Box.insert(0, '') #Insert blank for user input
        Search_Box.config(fg = 'black')
def on_search_input_focusout(event):
    if Search_var.get () != 'Search The Web ':
        Search_Box.config(fg = 'black')
    if Search_var.get() == '' or Search_var.get() == 'Search The Web ' or event == "None":
        Search_var.set('Search The Web ')
        Search_Box.config(fg = "#999999")

#Voice Search
mixer.init()
def voice():
    micButTon.config(state=DISABLED)
    mixer.music.load(resource_path('Start_Music.mp3'))
    mixer.music.play()
    sr=speech_recognition.Recognizer()
    with speech_recognition.Microphone()as m:
        try:
            sr.adjust_for_ambient_noise(m, duration=0.2)
            audio=sr.listen(m)
            message = sr.recognize_google(audio)
            Search_var.set(message)
            mixer.music.load(resource_path('End_Music.mp3'))
            mixer.music.play()
            Search_Box.config(fg = 'black')
        except:
            N_Label = Label(MainWindow,text="Someting Went Wrong !! Please Try Again\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
            mixer.music.load(resource_path('End_Music.mp3'))
            mixer.music.play()
            N_Label.pack(side=BOTTOM)
            N_Label.after(3500, N_Label.destroy)
            N_Label.focus_set()
            Search_var.set("Search The Web ")
            on_search_input_focusout("None")
    micButTon.config(state=NORMAL)

def ch_button (e):
    if CheckVar1.get() == 1:
        CheckVar1.set(1)
        CheckVar2.set(0)
        CheckVar3.set(0)
        CheckVar4.set(0)
        CheckVar5.set(0)
    if CheckVar2.get() == 1 and CheckVar3.get() == 1 and CheckVar4.get() == 1 and CheckVar5.get() == 1 :
        CheckVar1.set(1)
        CheckVar2.set(0)
        CheckVar3.set(0)
        CheckVar4.set(0)
        CheckVar5.set(0)


#Home_Screen_frame
H_frame = Frame(MainWindow,bg=Background_Main)
H_frame2 = Frame(H_frame,bg=Background_Main)
H_frame3 = Frame(H_frame,bg=Background_Main)
H_frame4 = Frame(H_frame,bg=Background_Main)

# Create Buttons
Search_Label = Label(H_frame,text="Search",font=("Comic Sans MS", 56, "bold"),bg=Background_Main)
Search_Label.pack()
Label(H_frame,text=" ",bg=Background_Main).pack()

Search_Box = Entry(H_frame,textvariable=Search_var,foreground="#999999",font=("Sitka Small",14),width=60)
Search_Box.bind('<FocusIn>', on_search_input_click)
Search_Box.bind('<FocusOut>', on_search_input_focusout)
Search_Box.pack()

micImage=PhotoImage(file=(resource_path('mic.png')))
micButTon=Button(H_frame,image=micImage,bd=0,cursor='hand2',height=27,command=voice,bg="white",activebackground="white")
micButTon.place(y=133,x=750)

Label(H_frame2,text="Scrapping From",font=("arial",12),bg=Background_Main).pack(side=LEFT,anchor=E)
C1 = Checkbutton(H_frame2,cursor="hand2", text = "All",font=("arial",12) ,variable = CheckVar1,command=lambda:ch_button(1), onvalue = 1, offvalue = 0, height=3, width = 10,bg=Background_Main,activebackground=Background_Main)
C2 = Checkbutton(H_frame2,cursor="hand2", text = "Google",font=("arial",12) , variable = CheckVar2,command=lambda:ch_button(2), onvalue = 1, offvalue = 0, height=3, width = 10,bg=Background_Main,activebackground=Background_Main)
C3 = Checkbutton(H_frame2,cursor="hand2", text = "Yahoo",font=("arial",12) , variable = CheckVar3,command=lambda:ch_button(3), onvalue = 1, offvalue = 0, height=3, width = 10,bg=Background_Main,activebackground=Background_Main)
C4 = Checkbutton(H_frame2,cursor="hand2", text = "DuckDuckGo",font=("arial",12) , variable = CheckVar4,command=lambda:ch_button(4), onvalue = 1, offvalue = 0, height=3, width = 10,bg=Background_Main,activebackground=Background_Main)
C5 = Checkbutton(H_frame2,cursor="hand2", text = "Bing",font=("arial",12) , variable = CheckVar5,command=lambda:ch_button(5), onvalue = 1, offvalue = 0, height=3, width = 10,bg=Background_Main,activebackground=Background_Main)

C1.pack(side=LEFT)
C2.pack(side=LEFT)
C3.pack(side=LEFT)
C4.pack(side=LEFT)
C5.pack(side=LEFT)

H_frame4.pack(side=BOTTOM,anchor=CENTER)
Label(H_frame,text=" ",font=("Arial",3),bg=Background_Main).pack(side=BOTTOM)
H_frame3.pack(side=BOTTOM)
Label(H_frame,text=" ",font=("Arial",1),bg=Background_Main).pack(side=BOTTOM)
H_frame2.pack(side=BOTTOM)

#-----------------------------------------------------------------------------
#Main Home Screen
def home():
    MainWindow.config(bg=Background_Main)
    His_frame.forget()
    Setting_frame.forget()
    Setting_frame.place(x=15*5000,y=15*5000)
    His_frame.place(x=15*5000,y=15*5000)
    H_frame.place(x=0,y=-68.5,relx=.5, rely=.5,anchor= CENTER)
    CheckVar1.set(1)
    bak_button_HOME.place(x=15*5000,y=15*5000)
    del_button_His.place(x=15*5000,y=15*5000)
    Proxy_Save.place(x=15*5000,y=15*5000)
    Search_var.set("Search The Web ")
    on_search_input_focusout("None")
    History_table.focus_set()
    bak_button_HOME.config(command=home)

#Go To History Page
def view_history():
    H_frame.place(x=15*5000,y=15*5000)
    His_frame.pack(fill=BOTH,expand=1)
    bak_button_HOME.place(x=10,y=5)
    del_button_His.place(x=55,y=5)
    History_table.delete(*History_table.get_children())
    if (os.path.isfile(Db_Path)) == True:
        conn = sqlite3.connect(Db_Path)
        cursor = conn.execute("SELECT * FROM History ORDER BY DATE DESC, TIME DESC")
        for row in cursor:
            a = row[0]
            b = row[1]
            c = row[2]
            d = row[3]
            History_table.insert('',END,values=[a,b,c,d])
        conn.close()

#Go to Settings Page
def setting_page():
    Proxy_Save.place(y=188,x=600)
    H_frame.place(x=15*5000,y=15*5000)
    His_frame.forget()
    Setting_frame.pack(fill=BOTH,expand=1)
    bak_button_HOME.place(x=10,y=5)
    if Proxy_Load == False :
        RadioNutton_VAR.set(1)
        Address_Entry.config(state=DISABLED)
        Proxy_Save.config(state=DISABLED)
        Address_Entry_var.set('Hint:- protocol://ip:port ')
        Address_Entry.config(fg = "#999999")
        on_Address_input_focusout("None")
        MainWindow.focus_set()


#Main Search Function
def main_Search():
    def DestryTab():
        label_line_progress.destroy()
        tabControl.destroy()
        home()

    bak_button_HOME.place(x=10,y=5)
    bak_button_HOME.config(command=DestryTab)
    bak_button_HOME.config(state=DISABLED)
    tabControl = ttk.Notebook(MainWindow)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    Query = Search_var.get()

    tabControl.add(tab1, text ='Normal Result')
    tabControl.add(tab2, text ='Links')

    label_line_progress = Label(MainWindow, bg=Background_Main)
    label_line_progress.pack(side=TOP,anchor=E)
    Label(label_line_progress,text="Please Wait ",font =("Courier", 14),pady=10,bg=Background_Main).pack(side=LEFT)

    line_progress = ttk.Progressbar(label_line_progress,length=250)
    line_progress.start(100)
    line_progress.pack(fill='x', expand=True, pady=10)

    tabControl.pack(fill=BOTH,expand=1)

    def web_results ():
        start = time.time()
        webScrapping.downloadImage(Query,4) #Query
        w= 258
        h=180

        data = (webScrapping.wikiResult(Query)) #Query
        # if date == "Desired Result Not Found":
            # data = (webScrapping.googleSearch("Indian Army")) #Query

        imageContainer = Frame(tab1)
        imageContainer.pack(anchor='w')
        #loading images
        img0 = ImageTk.PhotoImage(PIL.Image.open(temp_directory+'img0.jpg').resize((w,h), PIL.Image.ANTIALIAS))
        img1 = ImageTk.PhotoImage(PIL.Image.open(temp_directory+'img1.jpg').resize((w,h), PIL.Image.ANTIALIAS))
        img2 = ImageTk.PhotoImage(PIL.Image.open(temp_directory+'img2.jpg').resize((w,h), PIL.Image.ANTIALIAS))
        img3 = ImageTk.PhotoImage(PIL.Image.open(temp_directory+'img3.jpg').resize((w,h), PIL.Image.ANTIALIAS))
        #Displaying
        L1= Label(imageContainer, image=img0)
        L1.image = img0
        L1.pack(side=LEFT)

        L2= Label(imageContainer, image=img1)
        L2.image = img1
        L2.pack(side=LEFT)

        L3= Label(imageContainer, image=img2)
        L3.image = img2
        L3.pack(side=LEFT)

        L4= Label(imageContainer, image=img3)
        L4.image = img3
        L4.pack(side=LEFT)

        scroll = Scrollbar(tab1)
        scroll.pack(side=RIGHT, fill=Y)
        T = Text(tab1, yscrollcommand=scroll.set,wrap = WORD,state='disabled',spacing2=5,spacing1=5,font =("Consolas", 12, "italic"))
        scroll.config(command=T.yview)

        def typeit(widget, index, string):
            widget.configure(state='normal')
            if len(string) > 0:
                widget.insert(index, string[0])
            if len(string) > 1:
                # compute index of next char
                index = widget.index("%s + 1 char" % index)
                # type the next character in half a second
                widget.after(10, typeit, widget, index, string[1:])
            widget.configure(state='disabled')
            widget.see(END)

        typeit(T, "1.0", data)

        # Create label
        l = Label(tab1, text = "Search Result (as simple query)")
        l.config(font =("Courier", 14))


        l.pack()
        T.pack(expand=TRUE,fill=BOTH)

        #---------------------------------------------------------

        if Address_Entry_var.get() != "Hint:- protocol://ip:port ":         #Proxy
            proxy = Address_Entry_var.get()
        else:
            proxy = None
        if clicked.get == "Yes":            #Ignore Duplicates
            i=True
        else:
            i=False
        p=current_value.get()               # Page Limit
        f=None                              # Filter Results [url, title, text, host]
        o='csv'                             #Save Format
        n = temp_directory+"Temporary"      #Output Path
        q = Query                           #Query
        en = ""
        if CheckVar1.get() == 1:
            en = "Google,Yahoo,DuckDuckGo,Bing"
        else:
            if CheckVar2.get() == 1:
                en=en+'Google,'
            if CheckVar3.get() == 1:
                en=en+'Yahoo,'
            if CheckVar4.get() == 1:
                en=en+'DuckDuckGo,'
            if CheckVar5.get() == 1:
                en=en+'Bing,'
            en=en[:-1]
        e = en
        timeout = config.TIMEOUT + (10 * bool(proxy))
        engines = [
            e.strip() for e in e.lower().split(',')
            if e.strip() in search_engines_dict or e.strip() == 'all'
        ]
        if not engines:
            print('Please choose a search engine: ' + ', '.join(search_engines_dict))
        else:
            if 'all' in engines:
                engine = AllSearchEngines(proxy, timeout)
            elif len(engines) > 1:
                engine = MultipleSearchEngines(engines, proxy, timeout)
            else:
                engine = search_engines_dict[engines[0]](proxy, timeout)
            engine.ignore_duplicate_urls = i
            if f:
                engine.set_search_operator(f)
            engine.search(q, p)
            engine.output(o, n)

            scrollbar_x = Scrollbar(tab2,orient=HORIZONTAL)
            scrollbar_y = Scrollbar(tab2,orient=VERTICAL)

            table = ttk.Treeview(tab2,style = "Treeview",columns =("No.","DOMAIN", "URL", "TITLE", "TEXT"),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)

            table.heading("No.",text="Num.")
            table.heading("DOMAIN",text="Domain's")
            table.heading("URL",text="Url's")
            table.heading("TITLE",text="Title's")
            table.heading("TEXT",text="Text's")

            table["displaycolumns"]=("No.","DOMAIN", "URL", "TITLE")
            table["show"] = "headings"

            table.column("No.",anchor='center',width=60,stretch=0)
            table.column("DOMAIN",anchor='center')
            table.column("URL",anchor='center')
            table.column("TITLE",anchor='center')
            table.column("TEXT",anchor='center')

            scrollbar_x.pack(side=BOTTOM,fill=X)
            scrollbar_y.pack(side=RIGHT,fill=Y)

            scrollbar_x.configure(command=table.xview)
            scrollbar_y.configure(command=table.yview)

            table.pack(fill=BOTH,expand=1)

            filename= temp_directory+'Temporary.csv'

            def highlight_row(event):
                tree = event.widget
                item = tree.identify_row(event.y)
                tree.tk.call(tree, "tag", "remove", "highlight")
                tree.tk.call(tree, "tag", "add", "highlight", item)
            table.tag_configure('highlight', background='lightblue')
            table.bind("<Motion>", highlight_row)

            def open_link_from_treeview(tree, event):
                selection = tree.selection()
                column = tree.identify_column(event.x)
                column_no = int(column.replace("#", "")) - 1
                if column_no == 1 or column_no == 2:
                    copy_values = []
                    for each in selection:
                        try:
                            value = tree.item(each)["values"][column_no]
                            copy_values.append(str(value))
                        except:
                            pass
                    copy_string = "\n".join(copy_values)
                    webbrowser.open(copy_string)
            table.bind("<Button-1>", lambda x: open_link_from_treeview(table, x))

            def copy_from_treeview(tree, event):
                selection = tree.selection()
                column = tree.identify_column(event.x)
                column_no = int(column.replace("#", "")) - 1

                if column_no != 0:
                    copy_values = []
                    for each in selection:
                        try:
                            value = tree.item(each)["values"][column_no]
                            copy_values.append(str(value))
                        except:
                            pass
                    copy_string = "\n".join(copy_values)
                    pyperclip.copy(copy_string)
            table.bind("<Control-Key-c>", lambda x: copy_from_treeview(table, x))

            n = 1
            with open(filename,encoding="utf8") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    D = row['domain']
                    U = row['URL']
                    Title = row['title']
                    Txt = row['text']
                    table.insert('',END,values=[n,D, U, Title, Txt])
                    n = n+1

        line_progress.stop()
        end = time.time()
        for widget in label_line_progress.winfo_children():
            widget.destroy()
        #Calculate Run Time
        sec = int(end - start)
        seconds = sec % (24 * 3600)
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        res = str("%02d Minute, %02d Seconds." % (minutes, seconds))

        Lab = Label(label_line_progress,text="Total Time Taken "+res,bg=Background_Main,font =("Courier", 12),pady=12)
        Lab.pack(side=LEFT)
        Lab.after(10000, Lab.destroy)
        cleared_temp()
        bak_button_HOME.config(state=NORMAL)

    try:
        Thread(target=web_results).start()
    except exceptions as what_is_wrong:
        print(what_is_wrong)


#Delete History Button Function
def del_history():
    if (os.path.isfile(Db_Path)) == True:
        ans = messagebox.askquestion("Clear History","Do you want to clearer the History ?")
        if ans == "yes":
            os.remove(Db_Path)
            History_table.delete(*History_table.get_children())
    else:
        N_Label = Label(MainWindow,text="No History !!",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
        N_Label.pack(side=BOTTOM)
        N_Label.after(1600, N_Label.destroy)

#Add History Button Function
def add_History():
    today = date.today()
    now = datetime.now()
    current_Date = today.strftime("%d/%m/%Y")
    current_Time = now.strftime("%H:%M:%S")
    q = Search_var.get()
    en = ""
    if CheckVar1.get() == 1:
        en = "Google, Yahoo, DuckDuckGo, Bing"
    else:
        if CheckVar2.get() == 1:
            en=en+'Google '
        if CheckVar3.get() == 1:
            en=en+'Yahoo '
        if CheckVar4.get() == 1:
            en=en+'DuckDuckGo '
        if CheckVar5.get() == 1:
            en=en+'Bing '
        en=en[:-1]
    if (os.path.isfile(Db_Path)) == False:
        conn = sqlite3.connect(Db_Path)
        conn.execute('''CREATE TABLE History(DATE TEXT NOT NULL, TIME TEXT NOT NULL, QUERY TEXT NOT NULL, ENGINE TEXT NOT NULL);''')
        conn.execute("INSERT INTO History (DATE, TIME, QUERY, ENGINE) values(?,?,?,?)",(current_Date, current_Time, q, en))
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect(Db_Path)
        conn.execute("INSERT INTO History (DATE, TIME, QUERY, ENGINE) values(?,?,?,?)",(current_Date, current_Time, q, en))
        conn.commit()
        conn.close()


#Search Button Function
def search_button(e):
    validation = False
    #Validation
    if CheckVar1.get() == 0 and CheckVar2.get() == 0 and CheckVar3.get() == 0 and CheckVar4.get() == 0 and CheckVar5.get() == 0:
        validation = False
        N_Label = Label(MainWindow,text="No Search Engine Is Selected\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
        N_Label.pack(side=BOTTOM)
        N_Label.after(1600, N_Label.destroy)
    else:
        if Search_var.get()!="Search The Web ":
            v = Search_var.get().replace(" ", "")
            if len(v)>1:
                validation = True
            else:
                validation = False
                N_Label = Label(MainWindow,text="Invalid Query\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
                N_Label.pack(side=BOTTOM)
                N_Label.after(1600, N_Label.destroy)
        else:
            validation = False
            N_Label = Label(MainWindow,text="Nothing To Search\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
            N_Label.pack(side=BOTTOM)
            N_Label.after(1600, N_Label.destroy)
    if validation == True:
        add_History()
        main_Search()

def setting_button_on_enter(e):
    Setting_Button.config(foreground="RED")

def setting_button_on_leave(e):
    Setting_Button.config(foreground="BLUE")


#----------------------------------------------------------------------------

Label(His_frame,text=" Search History ",font=("LucidiaSans",18,"bold","underline"),bg=Background_Main).pack(side=TOP)
Label(His_frame,text=" ",pady=2,bg=Background_Main).pack(side=TOP)

bak_icon=PhotoImage(file=(resource_path('back_Icon.png')))
bak_button_HOME = Button(MainWindow,cursor="hand2",image=bak_icon,command=home)

del_icon=PhotoImage(file=(resource_path('del_icon.png')))
del_button_His = Button(MainWindow,cursor="hand2",image=del_icon,command=del_history)

scrollbar_billCon_x = Scrollbar(His_frame,orient=HORIZONTAL)
scrollbar_billCon_y = Scrollbar(His_frame,orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading",font=("arial",13, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)

History_table = ttk.Treeview(His_frame,style = "Treeview",
            columns =("date","time","query","eng"),height=7,xscrollcommand=scrollbar_billCon_x.set,
            yscrollcommand=scrollbar_billCon_y.set)

History_table.heading("date",text="Date")
History_table.heading("time",text="Time")
History_table.heading("query",text="Query")
History_table.heading("eng",text="Engine")

History_table["displaycolumns"]=("date", "time","query","eng")
History_table["show"] = "headings"

History_table.column("date",anchor='center')
History_table.column("time",width=160,stretch=0,anchor='center')
History_table.column("query",width=480,anchor='center')
History_table.column("eng",width=250,stretch=0,anchor='center')


scrollbar_billCon_x.pack(side=BOTTOM,fill=X)
scrollbar_billCon_y.pack(side=RIGHT,fill=Y)

scrollbar_billCon_x.configure(command=History_table.xview)
scrollbar_billCon_y.configure(command=History_table.yview)

History_table.pack(fill=BOTH,expand=1)

#-----------------------------------------------------------------------------

def on_Address_input_click(e):
    if Address_Entry_var.get() == 'Hint:- protocol://ip:port ':
        Address_Entry.delete(0, "end") # delete all the text in the entry
        Address_Entry.insert(0, '') #Insert blank for user input
        Address_Entry.config(fg = 'black')

def on_Address_input_focusout(e):
    if Address_Entry_var.get () != 'Hint:- protocol://ip:port ':
        Address_Entry.config(fg = 'black')
    if Address_Entry_var.get() == '' or Address_Entry_var.get() == 'Hint:- protocol://ip:port ' or e == "None":
        Address_Entry_var.set('Hint:- protocol://ip:port ')
        Address_Entry.config(fg = "#999999")

def proxy_Button():
    global Proxy_Load
    if RadioNutton_VAR.get() == 2:
        Address_Entry.config(state=NORMAL)
        Proxy_Save.config(state=NORMAL)
    if RadioNutton_VAR.get() == 1:
        Address_Entry.config(state=DISABLED)
        Proxy_Save.config(state=DISABLED)
        Address_Entry_var.set('Hint:- protocol://ip:port ')
        Address_Entry.config(fg = "#999999")
        on_Address_input_focusout("None")
        MainWindow.focus_set()
        Proxy_Load = True

def proxy_save():
    global Proxy_Load
    if Address_Entry_var.get() == '' or Address_Entry_var.get() == 'Hint:- protocol://ip:port ':
        N_Label = Label(MainWindow,text="Please Enter A Proxy Server Address\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
        N_Label.pack(side=BOTTOM)
        N_Label.after(3500, N_Label.destroy)
        N_Label.focus_set()
        Proxy_Load = False
    else:
        N_Label = Label(MainWindow,text="Proxy Server Saved\n",font=("georgia",13),state=DISABLED,disabledforeground="Black",bg=Background_Main)
        N_Label.pack(side=BOTTOM)
        N_Label.after(3500, N_Label.destroy)
        N_Label.focus_set()
        Proxy_Load = True

def proupdate_value(e):
    value = str(current_value.get())
    show_value.config(text="No Of Pages To Be Scrapped Is Set To "+value)

Label(Setting_frame,text=" ",font=("LucidiaSans",1),pady=1,bg=Background_Main).pack(side=TOP)
Label(Setting_frame,text="Settings",font=("LucidiaSans",19,"bold","underline"),background=Background_Main).pack(side=TOP)
Label(Setting_frame,text=" ",pady=2,bg=Background_Main).pack(side=TOP)

Radio_Frame = Frame(Setting_frame,bg=Background_Main)
Label(Setting_frame,text=" ",padx=15,bg=Background_Main).pack(side=LEFT)
Radio_Frame.pack(anchor=W,fill=BOTH)
Radio_Frame2 = Frame(Setting_frame,bg=Background_Main)
Radio_Frame2.pack(side=TOP,fill=X)
Sub_Setting_Frame = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",3),bg=Background_Main).pack()
Sub_Setting_Frame2 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame2.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",3),bg=Background_Main).pack()
Sub_Setting_Frame3 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame3.pack(side=TOP,fill=X)
Sub_Setting_Frame4 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame4.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",3),bg=Background_Main).pack()
Drop_Frame = Frame(Setting_frame,bg=Background_Main)
Drop_Frame.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",14),bg=Background_Main).pack()
Sub_Setting_Frame5 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame5.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",1),bg=Background_Main).pack()
Sub_Setting_Frame6 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame6.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",6),bg=Background_Main).pack()
Sub_Setting_Frame7 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame7.pack(side=TOP,fill=X)
Label(Setting_frame,text="",font=("arial",10),bg=Background_Main).pack()
Sub_Setting_Frame8 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame8.pack(side=TOP,fill=X)
Sub_Setting_Frame9 = Frame(Setting_frame,bg=Background_Main)
Sub_Setting_Frame9.pack(side=BOTTOM,fill=X)

R1 = Radiobutton(Radio_Frame,cursor="hand2", text="No Proxy",font=('MSReferenceSansSerif',14,"bold") ,variable=RadioNutton_VAR, value=1, command=proxy_Button,bg=Background_Main,activebackground=Background_Main)
R2 = Radiobutton(Radio_Frame2,cursor="hand2", text="Use A Manual Proxy Server",font=('MSReferenceSansSerif',14,"bold") ,pady=10, variable=RadioNutton_VAR, value=2, command=proxy_Button,bg=Background_Main,activebackground=Background_Main)

R1.pack(side=LEFT)
R2.pack(side=LEFT)

Label(Sub_Setting_Frame,text="Enter Proxy Server Address And Port",font=("FranklinGothicMedium",12),bg=Background_Main).pack(side=LEFT)

Address_Entry = Entry(Sub_Setting_Frame2,foreground="#999999",textvariable=Address_Entry_var,font=("Sitka Small",13),width=45)
Address_Entry.pack(side=LEFT)
Address_Entry.bind('<FocusIn>', on_Address_input_click)
Address_Entry.bind('<FocusOut>', on_Address_input_focusout)

Proxy_Save = Button(MainWindow,cursor="hand2",text="Save",font=("LucidiaBright",10,"bold"),command=proxy_save)

Label(Sub_Setting_Frame3,text="\nIgnore Duplicates Search Results ?",font=("FranklinGothicMedium",14),bg=Background_Main).pack(side=LEFT)
Label(Sub_Setting_Frame4,text="(It Comes Handy When Multiple Search Engines Are Used)",font=("FranklinGothicMedium",12),bg=Background_Main).pack(side=LEFT)

options = ["Yes","No",]
drop_menu = OptionMenu(Drop_Frame,clicked,*options,)
drop_menu.pack(side=LEFT)
drop_menu.config(font=("LucidiaBright",10,"bold"),width=8)
menu = Drop_Frame.nametowidget(drop_menu.menuname)
menu.config(font=("LucidiaBright",10,"bold"))

Label(Sub_Setting_Frame5,text="No Of Pages To Scrapped (Default Is 5, Maximum 50)",font=("FranklinGothicMedium",14),bg=Background_Main).pack(side=LEFT)
warning_Icon=PhotoImage(file=(resource_path('Warning.png')))
Label(Sub_Setting_Frame6,image=warning_Icon,compound=LEFT,text=" Increasing Page Number Will Slow Down Search Time.... ",font=("FranklinGothicMedium",12),bg=Background_Main).pack(side=LEFT)

Scale(Sub_Setting_Frame7,cursor="hand2",bg="#D8D8D8",length=540,showvalue=0,from_= 1, to=50,orient='horizontal',variable=current_value,font=("FranklinGothicMedium",14),command=proupdate_value).pack(side=LEFT)#,command=slider_changed
show_value = Label(Sub_Setting_Frame8,text="No Of Pages To Be Scrapped Is Set To 5",font=("FranklinGothicMedium",13),bg=Background_Main)
show_value.pack(side=LEFT)

Label(Sub_Setting_Frame9,text="Developed By Hrishikesh Patra",font=("arial",8),bg=Background_Main).pack(side=RIGHT)

#-----------------------------------------------------------------------------

searchbutton = Button(H_frame3,text="Search",font=("LucidiaBright",13,"bold"),command=lambda:search_button(None),padx=15)
searchbutton.pack(side=LEFT)
Label(H_frame3,text=" ",padx=7,bg=Background_Main).pack(side=LEFT)
History_Button = Button(H_frame3,text="History",font=("LucidiaBright",13,"bold"),command=view_history,padx=15)
History_Button.pack(side=LEFT)
Setting_Button = Button(H_frame4,text="Change Search Settings",relief=SUNKEN,bd=0,font=("PalaceScriptMT",11,"bold","italic"),bg=Background_Main,activebackground=Background_Main,foreground="BLUE",activeforeground="RED",command=setting_page)
Setting_Button.pack(side=BOTTOM)
Setting_Button.bind("<Enter>", setting_button_on_enter)
Setting_Button.bind("<Leave>", setting_button_on_leave)
Setting_Button.bind('<Return>', search_button)

def on_closing():
    ans = messagebox.askquestion("Quit", "Do you want to quit?")
    if ans == "yes":
        pid = os.getpid()
        os.kill(pid,signal.SIGTERM)

#Screen Size And Measurement Part
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
screen_width_ADJ = (screen_width/1.3)
screen_height_ADJ = (screen_height/1.3)
ws = MainWindow.winfo_screenwidth()
hs = MainWindow.winfo_screenheight()
w = int(screen_width_ADJ)
h = int(screen_height_ADJ)
# calculate position x, y
x = (ws/2) - (w/2)
y = (hs/2.20) - (h/2)

#Screen Re-Size Mini/Max
def resize_event(event):
    if MainWindow.state() == 'zoomed':
        MainWindow.geometry('%dx%d+%d+%d' % (screen_width, screen_height, x, y))
    if MainWindow.state() == 'normal':
        MainWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

def Shortcut_F11(event):
    if MainWindow.state() == 'normal':
        MainWindow.state('zoomed')
        resize_event(None)
    elif MainWindow.state() == 'zoomed':
        MainWindow.state('normal')
        resize_event(None)

MainWindow.bind("<F11>", Shortcut_F11)
MainWindow.title("Search Engine (Indian Army Secure Coding 3rd Round Challenge)")
MainWindow.bind("<Configure>", resize_event)
MainWindow.protocol("WM_DELETE_WINDOW", on_closing)
warnings.filterwarnings("ignore")

#Run
if __name__ == "__main__":
    cleared_temp()
    home()
    MainWindow.mainloop()