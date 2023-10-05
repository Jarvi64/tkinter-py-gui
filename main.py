from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

def clear_input():
    hostname_entry.delete(0, END)
    Brand_entry.delete(0, END)
    ram_entry.delete(0, END)
    flash_entry.delete(0, END)

def add_router():  
    hostname = hostname_entry.get()
    if hostname: 
        brand = Brand_entry.get()  
        if brand:
            ram = ram_entry.get()
            if ram:
                flash = flash_entry.get()
                if flash:
                    conn = sqlite3.connect('data.db')
                    table_creation_query = '''CREATE TABLE IF NOT EXISTS Router_Data
                                             (hostname TEXT, brand TEXT, ram INT, flash INT)
                                          '''
                    conn.execute(table_creation_query)

                    # Inserting Data
                    data_insert_query = '''INSERT INTO Router_Data(hostname, brand, ram, flash)
                                           VALUES (?, ?, ?, ?)'''
                    data_insert_tuple = (hostname, brand, ram, flash)

                    cursor = conn.cursor()
                    cursor.execute(data_insert_query, data_insert_tuple)
                    conn.commit()
                    conn.close()    
                    tree.insert("", "end", values=(hostname, brand, ram, flash))
                    clear_input()
                else:
                    messagebox.showwarning(title="Empty flash", message="Flash Field is empty!")
            else:
                messagebox.showwarning(title="Empty RAM", message="RAM Field is empty!")       
        else:
            messagebox.showwarning(title="Empty brand", message="Brand Field is empty!")    
    else:
        messagebox.showwarning(title="Empty hostname", message="Host name is empty!")


def remove_router():
    selected_item = tree.selection()
    if selected_item:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Get the hostname of the selected row
        selected_hostname = tree.item(selected_item, 'values')[0]

        # Delete the row from the database
        cursor.execute("DELETE FROM Router_Data WHERE hostname=?", (selected_hostname,))  # Note the comma after selected_hostname
        conn.commit()

        # Delete the selected item from the tree
        tree.delete(selected_item)

        conn.close()
        clear_input()
    else:
        messagebox.showwarning(title="No Selection", message="No router selected!")

def update_router():
    selected_item = tree.selection()
    if selected_item:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        selected_hostname = tree.item(selected_item, 'values')[0]

        hostname = hostname_entry.get()
        brand = Brand_entry.get()
        ram = ram_entry.get()
        flash = flash_entry.get()

        # Updating the record in the database
        update_query = '''UPDATE Router_Data 
                          SET hostname=?, brand=?, ram=?, flash=? 
                          WHERE hostname=?'''
        update_data = (hostname, brand, ram, flash, selected_hostname)

        cursor.execute(update_query, update_data)
        conn.commit()

        tree.item(selected_item, values=(hostname, brand, ram, flash))

        conn.close()
        clear_input()
    else:
        messagebox.showwarning(title="No Selection", message="No router selected!")

def populate_fields():
    selected_item = tree.selection()  
    if selected_item:
        selected_data = tree.item(selected_item, 'values')  
        hostname_entry.delete(0, END)  
        hostname_entry.insert(0, selected_data[0])  
        Brand_entry.delete(0, END)  
        Brand_entry.insert(0, selected_data[1])  
        ram_entry.delete(0, END)  
        ram_entry.insert(0, selected_data[2])  
        flash_entry.delete(0, END) 
        flash_entry.insert(0, selected_data[3])  

def search_host():
    search_host = search_by_host_entry.get()
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    search_query = "SELECT * FROM Router_Data WHERE hostname LIKE ?"
    cursor.execute(search_query, ('%' + search_host + '%',))

    # Fetch the matching rows
    rows = cursor.fetchall()

    # Clear existing items in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert search results into the Treeview
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()    

def search_query():
    custom_query = search_by_query_entry.get()
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:
        cursor.execute(custom_query)
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error executing query: {e}")

    conn.close()

window = Tk()
window.title("Router Manager")
common_font = ("Arial", 10)  # You can adjust the font family and size here
window.option_add("*Font", common_font)

frame = Frame(window)
frame.pack()

#Search frame

search_frame = LabelFrame(frame,text="Serach Router")
search_frame.grid(row=0,column=0,padx=10,pady=10)

search_by_host_label = Label(search_frame,text="Search by Host Name").grid(row=0,column=0)
search_by_query_label = Label(search_frame,text="Search by Query").grid(row=1,column=0)

default_query = StringVar()
default_query.set("SELECT * FROM Router_Data")

search_by_host_entry = Entry(search_frame,width=50)
search_by_host_entry.grid(row=0,column=1)

search_by_query_entry = Entry(search_frame, textvariable=default_query,width=50)
search_by_query_entry.grid(row=1, column=1)

search_by_host_button = Button(search_frame,text="search",command=search_host).grid(row=0,column=2)
search_by_query_button = Button(search_frame,text="search",command=search_query).grid(row=1,column=2)

for widget in search_frame.winfo_children():

    widget.grid_configure(padx=32,pady=10)

#Entry frame

entry_frame = LabelFrame(frame,text="Enter Data")
entry_frame.grid(row=1,column=0,padx=20,pady=10)

hostname_label = Label(entry_frame,text="Host Name").grid(row=0,column=0)
hostname_entry = Entry(entry_frame,width=25)
hostname_entry.grid(row=0,column=1)

Brand_label = Label(entry_frame,text="Brand").grid(row=0,column=2)
Brand_entry = Entry(entry_frame,width=25)
Brand_entry.grid(row=0,column=3)

ram_label = Label(entry_frame,text="RAM").grid(row=1,column=0)
ram_entry = Entry(entry_frame,width=25)
ram_entry.grid(row=1,column=1)

flash_label = Label(entry_frame,text="Flash").grid(row=1,column=2)
flash_entry = Entry(entry_frame,width=25)
flash_entry.grid(row=1,column=3)

add_router_btn = Button(entry_frame,text="Add Router",command=add_router).grid(row=2,column=0)
remove_router_btn = Button(entry_frame,text="Remove Router",command=remove_router).grid(row=2,column=1)
update_router_btn = Button(entry_frame,text="Update Router",command=update_router).grid(row=2,column=2)
clear_input_btn = Button(entry_frame,text="Clear Input",command=clear_input).grid(row=2,column=3)

for widget in entry_frame.winfo_children():
    widget.grid_configure(padx=24,pady=10)    

#Display frame

display_frame = LabelFrame(frame,text="Display Data")
display_frame.grid(row=2,column=0,padx=10,pady=10)

columns = ("host_name", "brand", "ram", "flash")
tree = ttk.Treeview(display_frame,columns=columns, show='headings')
tree.grid(row=0, column=0,padx=15,pady=14)

tree.heading('host_name', text='Host Name')
tree.heading('brand', text='Brand')
tree.heading('ram', text='RAM')
tree.heading('flash', text='FLASH')

scrollbar = ttk.Scrollbar(display_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Router_Data")
rows = cursor.fetchall()
    
for row in rows:
        tree.insert("", "end", values=row)
    
conn.close()
tree.bind('<ButtonRelease-1>', lambda event=None: populate_fields())

window.mainloop()