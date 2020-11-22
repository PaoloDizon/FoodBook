from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Treeview
import sqlite3





# create sqlite3 database

conn = sqlite3.connect(('JoeBook.db'))
print("opened the database")
cursor = conn.cursor()



def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

#search by foodtype
def search1():
    q2 = q.get()
    query = "SELECT restaurant, foodtype, occasion, location from resty WHERE foodtype LIKE '%"+q2+"%' "
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def search2():
    q3= bong.get()
    query = "SELECT restaurant, foodtype, occasion, location from resty WHERE occasion LIKE '%"+q3+"%' "
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def clear():
    query = "SELECT restaurant, foodtype, occasion, location from resty"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])

def update_restaurant():
    rname = t1.get()
    ftype = t2.get()
    occa = t3.get()
    loc = t4.get()

    if messagebox.askyesno("Confirm Update"):
        query ="UPDATE resty SET foodtype = ?, occasion = ?, location = ? WHERE restaurant = ?"
        cursor.execute(query, (ftype, occa, loc, rname))
        conn.commit()
        clear()
    else:
        return True


def add_new():
    rname = t1.get()
    ftype = t2.get()
    occa = t3.get()
    loc = t4.get()
    # query = '''INSERT INTO resty (restaurant, foodtype, occasion, location) VALUES(?, ?, ?, ?))'''
    # cursor.execute(query, (rname, ftype, occa, loc))
    cursor.execute("INSERT INTO resty(restaurant, foodtype, occasion, location) VALUES(?,?,?,?)", (rname, ftype, occa, loc))
    conn.commit()
    clear()


def delete_restaurant():
    rest_id = t1.get()
    if messagebox.askyesno("Confirm Deletion?"):
        # query = "DELETE FROM resty WHERE restaurant ="+rest_id
        cursor.execute("DELETE FROM resty WHERE restaurant = '" + rest_id + "'")
        conn.commit()
        clear()
    else:
        return True

root = Tk()
q = StringVar()
bong = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
# setup the different sections
wrapper1 = LabelFrame(root, text="Restaurant List")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text="Restaurant Data")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

# setup the treeview
trv = Treeview(wrapper1, columns=(1, 2, 3, 4), show="headings", height="20")
trv.pack()

trv.heading(1, text="Restaurant")
trv.heading(2, text="Food Type")
trv.heading(3, text="Occasion")
trv.heading(4, text="Location")

#doubleclick something from table, contents will go into user entry section
trv.bind('Double 1>', getrow)

#search section
#search by Foodtype
lbl = Label(wrapper2, text= "Search by Food Type")
lbl.pack(side=tk.LEFT, padx=10)
end = Entry(wrapper2, textvariable =q)
end.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text="Search", command=search1)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)

#search by occasion
lbl = Label(wrapper2, text= "Search by Occasion")
lbl.pack(side=tk.LEFT, padx=10)
end = Entry(wrapper2, textvariable =bong)
end.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text="Search", command=search2)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)

#show all contents of database in treeview
query = "SELECT restaurant, foodtype, occasion, location from resty"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

#User Entry
lbl1 = Label(wrapper3, text ="Restaurant Name")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1= Entry(wrapper3, textvariable=t1)
ent1.grid(row=0, column=1, padx=5 ,pady=3)

lbl2 = Label(wrapper3, text="Food Type")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(wrapper3, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=3)

lbl3 = Label(wrapper3, text="Occasion")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper3, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=3)

lbl4 = Label(wrapper3, text="Location")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(wrapper3, textvariable=t4)
ent4.grid(row=3, column=1, padx=5, pady=3)

upbtn= Button(wrapper3, text="Update", command=update_restaurant)
addbtn = Button(wrapper3, text="Add New", command=add_new)
delbtn = Button(wrapper3, text="Delete", command=delete_restaurant)

addbtn.grid(row=4, column=0, padx=5, pady=3)
upbtn.grid(row=4, column=1, padx=5, pady=3)
delbtn.grid(row=4, column=2, padx=5, pady=3)

# title the app, and setup size
root.title("Joe's Food Book")
root.geometry("800x800")
root.mainloop()

conn.close()

