from tkinter import *
from tkinter import ttk
from calendar import monthrange
from calendar import month_name
from cmath import nan
from queue import Empty
from datetime import datetime
import pymongo
import numpy as np
from datetime import *
import pandas as pd
import csv 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

global mycol
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["Cashbook2"]

def make_collect(month1):
    
    if month1 not in mydb.list_collection_names():
        mycol = mydb[month1]

root = Tk()
root.geometry('250x150')

def hello1():
    var.set("File Submitted")
    top3 = Toplevel(root)
    top3.geometry("70x70")
    new_load_button = Button(top3,text="New Load",command=new_load)
    new_load_button.grid(row=1,column=2,padx=4,pady=4)
    full_load_button = Button(top3,text="Full Load",command=full_load)
    full_load_button.grid(row=3,column=2,padx=2,pady=2)
def full_load():
    file1 = file_name.get()
    with open(file1,'r') as read_obj:
        csv_read = csv.reader(read_obj)
        listo = list(csv_read)
    j = 1
    for i in range(1,len(listo)):
        print(listo[i])
        
            
        
        make_collect(listo[i][0])
        mycol1 = mydb[listo[i][0]]
        
        if (listo[i][1] != ""):
            mydict = {"Wants":listo[i][1]}
            mycol1.insert_one(mydict)

        if (listo[i][2] != ""):
            mydict = {"Investment":listo[i][2]}
            mycol1.insert_one(mydict)

        if (listo[i][3] != ""):
            mydict = {"Needs":listo[i][3]}
            mycol1.insert_one(mydict)
        next_month = listo[j][0] 
        if(listo[i][0] != next_month):
            print(month_name1)
            month_name1.append(listo[i][0])
        
        if(j < (len(listo)-1)):
            j+=1
        else:
            next_month = " "
def new_load():
    file1 = file_name.get()
    with open(file1,'r') as read_obj:
        csv_read = csv.reader(read_obj)
        listo = list(csv_read)
    
    for i in range(1,len(listo)):
        print(listo[i])
        
            
        if listo[i][0] not in mydb.list_collection_names():
            
            make_collect(listo[i][0])
            mycol1 = mydb[listo[i][0]]
            
            if (listo[i][1] != ""):
                mydict = {"Wants":listo[i][1]}
                mycol1.insert_one(mydict)

            if (listo[i][2] != ""):
                mydict = {"Investment":listo[i][2]}
                mycol1.insert_one(mydict)

            if (listo[i][3] != ""):
                mydict = {"Needs":listo[i][3]}
                mycol1.insert_one(mydict)

def show_month_records():
    tree = ttk.Treeview(top, column=("Expense_Type", "Amount"), show='headings', height=20)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Expense_Type")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Amount")
    
    
    
    values_list=[]
    for i in mydb.list_collection_names():
        mycol = mydb[i]
        for j in mycol.find():
            values=[]
            m = list(j.values())
            values.append(m[1])
            n = list(j)
            values.append(n[1])
            values_list.append(values)
    for i in values_list:
        print(i)
        tree.insert('', 'end', text="1", values=(i[1], i[0]))
    tree.grid(row=4, column=1,columnspan=5)

def month_records():
    tree = ttk.Treeview(top, column=("Expense_Type", "Amount"), show='headings', height=20)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Expense_Type")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Amount")   
    records.set("Month Entered")
    values_list=[]
    
    mycol = mydb[month.get()]
    for j in mycol.find():
        values=[]
        m = list(j.values())
        values.append(m[1])
        n = list(j)
        values.append(n[1])
        values_list.append(values)

    tree.insert('','end',text="1",values=("Month",month.get()))
    for i in values_list:
        print(i)
        tree.insert('', 'end', text="1", values=(i[1], i[0]))
    tree.grid(row=4, column=1,columnspan=5)
    
            
def openrecord():
    global top
    top = Toplevel(root)
    top.geometry("450x500")
    spmonth = Label(top,text="Enter Specific Month")
    spmonth.grid(row=1,column=1)
    global month
    month = StringVar()
    enmonth = Entry(top,bd=4,textvariable=month)
    enmonth.grid(row=1,column=3)
    global records
    records = StringVar()
    records.set("Enter Month")
    show_records = Label(top,textvariable=records,bg="white")
    show_records.grid(row=2,column=3)
    spec_month = Button(top,text="Submit Month",command=month_records)
    spec_month.grid(row=2,column=1)
    all_records=Button(top,text="All records",command=show_month_records)
    all_records.grid(row=3,column=1)
    tree = ttk.Treeview(top, column=("Expense_Type", "Amount"), show='headings', height=20)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Expense_Type")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Amount")

def Analysis_allmonths():
    
    analys = {}
    wants=0
    inv = 0
    needs = 0
    sorted_month = list(mydb.list_collection_names())
    sorted_month = sorted(sorted_month,key=lambda m: datetime.strptime(m,"%B"))
    for j in sorted_month:
        if j != "ï»¿Month":
            print(j)
            mycol = mydb[j]
            w2 = 0
            iv =0
            nd = 0
            for i in mycol.find({},{"_id":0}):
                field = list(i.keys())
                value = list(i.values())
                if field[0] == "Wants":
                    
                    wants+=(int(value[0]))
                    w2+=(int(value[0]))
                if field[0] == "Investment":
                    
                    inv+=(int(value[0]))
                    iv+=(int(value[0]))
                if field[0] == "Needs":
                    
                    needs+=(int(value[0]))
                    nd+=(int(value[0]))
            
            analys[j] = w2+iv+nd
    month2 = list(analys.keys())
    print(analys)
    expense = list(analys.values())
    fig1 = plt.figure(figsize=(5,5))
    plt.plot(month2,expense)
    plt.tick_params(axis="both",labelsize=7)
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Expense Graph")
    fig2 = plt.figure(figsize=(5,5))
    exp_type = ["Wants","Investment","Needs"]
    exp = [wants,inv,needs]
    plt.bar(exp_type,exp,color="green",width=0.4)
    plt.xlabel("Expense Type")
    plt.ylabel("Expense Amount")
    plt.tick_params(axis="both",labelsize=7)
    plt.title("Expense Analysis")
    canvas = FigureCanvasTkAgg(fig2,master=top2)
    canvas.get_tk_widget().grid(row=5,column=3)
    canvas = FigureCanvasTkAgg(fig1,master=top2)
    canvas.get_tk_widget().grid(row=5,column=4)
    

def Analysis_month():
    ans3 = analy_month.get()
    mycol = mydb[ans3]
    analys = {}
    wants=0
    inv = 0
    needs = 0
    for i in mycol.find({},{"_id":0}):
        
        field = list(i.keys())
        
        value = list(i.values())
        if field[0] == "Wants":
                
            wants+=(int(value[0]))
        if field[0] == "Investment":    
                
            inv+=(int(value[0]))
        if field[0] == "Needs":
                
            needs+=(int(value[0]))
    print(wants,inv,needs)
    exp_type = ["Wants","Investment","Needs"]
    exp = [wants,inv,needs]
    fig = plt.figure(figsize=(5,5))
    plt.bar(exp_type,exp,color="green",width=0.4)
    plt.xlabel("Expense Type")
    plt.ylabel("Expense Amount")
    
    plt.title("Expense Analysis")
    canvas = FigureCanvasTkAgg(fig,master=top2)
    canvas.get_tk_widget().grid(row=5,column=3)
def showanaly():
    global top2
    top2 = Toplevel(root)
    top2.geometry("1300x600")
    spmonth = Label(top2,text="Enter Specific Month")
    spmonth.grid(row=1,column=1)
    global analy_month
    analy_month = StringVar()
    enmonth = Entry(top2,bd=4,textvariable=analy_month)
    enmonth.grid(row=1,column=3)
    spec_month = Button(top2,text="Submit Month",command=Analysis_month)
    spec_month.grid(row=2,column=1)
    all_records=Button(top2,text="All Month Analysis",command=Analysis_allmonths)
    all_records.grid(row=3,column=1)
Upperframe = Frame(root)
Upperframe.pack()
upframe = Frame(Upperframe)
upframe.pack()
Downframe = Frame(root)
Downframe.pack(side = BOTTOM)
global var,file_name
file_name = StringVar()
var = StringVar()

var.set("Not Submitted")
label = Label(upframe,text = "Enter the file path:")
label.grid(row = 1,column = 1)
global label2
label2 = Label(upframe,textvariable=var)
label2.grid(row=2,column=2)
submit_button = Button(upframe, text = "Submit",command=hello1)
submit_button.grid(row=3,column=1)
file_entry = Entry(upframe,bd=5,textvariable=file_name)
file_entry.grid(row=1, column=2, columnspan=3)


show_record = Button(upframe, text = "Show records",command=openrecord)
show_record.grid(row=4,column=1,columnspan=1)

show_analysis = Button(upframe, text="Show Analysis",command=showanaly)
show_analysis.grid(row=4,column=2,columnspan=1)





root.mainloop()
