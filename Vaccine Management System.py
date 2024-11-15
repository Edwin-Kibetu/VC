import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
# Connecting to Database
connector = sqlite3.connect('library.db')
cursor = connector.cursor()
connector.execute(
'CREATE TABLE IF NOT EXISTS Library (VC_NAME TEXT, VC_ID TEXT PRIMARY KEY NOT NULL, COMPANY_NAME TEXT, VC_STATUS TEXT, CARD_ID TEXT)' )


lf_bg = '#A3A3A3' 
rtf_bg = '#A6A6A6'
rbf_bg = '#A8A8A8'
btn_hlb_bg = '#707070'
lbl_font = ('Bookman Old Style', 13)
entry_font = ('Times New Roman', 12) # Font for all Entry widgets
btn_font = ('Gill Sans MT', 13)
# Initializing the main GUI window
root = Tk()
root.title('Vaccine Management System')
root.geometry('1010x530')
root.resizable(0, 0)
Label(root, text='VACCINE MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)
# StringVars
vc_status = StringVar()
vc_name = StringVar()
vc_id = StringVar()
company_name = StringVar()
card_id = StringVar()
# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)
RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)
RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)
# Left Frame
Label(left_frame, text='Vaccine Name', bg=lf_bg, font=lbl_font).place(x=98, y=25)
Entry(left_frame, width=25, font=entry_font, text=vc_name).place(x=45, y=55)
Label(left_frame, text='Vaccine ID', bg=lf_bg, font=lbl_font).place(x=110, y=105)
vc_id_entry = Entry(left_frame, width=25, font=entry_font, text=vc_id)
vc_id_entry.place(x=45, y=135)
Label(left_frame, text='Company Name', bg=lf_bg, font=lbl_font).place(x=90, y=185)
Entry(left_frame, width=25, font=entry_font, text=company_name).place(x=45, y=215)
Label(left_frame, text='Status of the Vaccine', bg=lf_bg, font=lbl_font).place(x=75, y=265)
dd = OptionMenu(left_frame, vc_status, *['Available', 'Issued'])
dd.configure(font=entry_font, width=12)
dd.place(x=75, y=300)
submit = Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=lambda:add_record)
submit.place(x=50, y=375)
clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=lambda: clear_fields)
clear.place(x=50, y=435)
# Right Top Frame
Button(RT_frame, text='Delete vaccine record', font=btn_font, bg=btn_hlb_bg, width=17, command=lambda: remove_record).place(x=8, y=30)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=lambda: delete_inventory).place(x=178, y=30)
Button(RT_frame, text='Update vaccine details', font=btn_font, bg=btn_hlb_bg, width=17,
command=lambda: update_record).place(x=348, y=30)
Button(RT_frame, text='Change Vaccine Availability', font=btn_font, bg=btn_hlb_bg, width=19, command=lambda: change_availability).place(x=518, y=30)
# Right Bottom Frame
Label(RB_frame, text='VACCINE INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)
tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Vaccine Name', 'Vaccine ID', 'Company', 'Status', 'Issuer Card ID'))
XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)
tree.heading('Vaccine Name', text='Vaccine Name', anchor=CENTER)
tree.heading('Vaccine ID', text='Vaccine ID', anchor=CENTER)
tree.heading('Company', text='Company', anchor=CENTER)
tree.heading('Status', text='Status of the Vaccine', anchor=CENTER)
tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=225, stretch=NO)
tree.column('#2', width=70, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=105, stretch=NO)
tree.column('#5', width=132, stretch=NO)
tree.place(y=30, x=0, relheight=0.9, relwidth=1)
command=lambda: clear_and_display()
# Finalizing the window


def add_record():
    global connector
    global vc_name, vc_id, company_name, vc_status
    if vc_status.get() == 'Issued':
       card_id.set(issuer_card())
    else:
       card_id.set('N/A')
    surety = mb.askyesno('Are you sure?',
                   'Are you sure this is the data you want to enter?\nPlease note that Vaccine ID cannot be changed in the future')
    if surety:
               try:
                connector.execute(
                 'INSERT INTO Library (VC_NAME, VC_ID, COMPANY_NAME, VC_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                        (vc_name.get(), vc_id.get(), company_name.get(), vc_status.get(), card_id.get()))
                connector.commit()
                clear_and_display()
     
                mb.showinfo('Record added', 'The new record was successfully added to your database')
               except sqlite3.IntegrityError:
                mb.showerror('Vaccine ID already in use!',
                              'The Vaccine ID you are trying to enter is already in the database, please alter that vaccine\'s record or check any discrepancies on your side')

def update_record():
   def update():
       global vc_status, vc_name, vc_id, company_name, card_id
       global connector, tree
       if vc_status.get() == 'Issued':
             card_id.set(issuer_card())
       else:
             card_id.set('N/A')
       cursor.execute('UPDATE Library SET VC_NAME=?, VC_STATUS=?, COMPANY_NAME=?, CARD_ID=? WHERE VC_ID=?', (vc_name.get(), vc_status.get(), company_name.get(), card_id.get(), vc_id.get()))
       connector.commit()
       clear_and_display()
       edit.destroy()
       vc_id_entry.config(state='normal')
       clear.config(state='normal')
       view_record()
       vc_id_entry.config(state='disable')
       clear.config(state='disable')
       edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
       edit.place(x=50, y=375)


def remove_record():
    if not tree.selection():
     mb.showerror('Error!', 'Please select an item from the database')
     return
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    cursor.execute('DELETE FROM Library WHERE VC_ID=?', (selection[1], ))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
    clear_and_display()

def delete_inventory():
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
     tree.delete(*tree.get_children())
     cursor.execute('DELETE FROM Library')
     connector.commit() 
    else:
     return

def change_availability():
    global card_id, tree, connector
    if not tree.selection():
        mb.showerror('Error!', 'Please select a vaccine from the database')
        return
    current_item = tree.focus()
    values = tree.item(current_item)
    VC_id = values['values'][1]
    VC_status = values["values"][3]
    if VC_status == 'Issued':
      surety = mb.askyesno('Is return confirmed?', 'Has the vaccine been returned to you?')
    if surety:
       cursor.execute('UPDATE Library SET vc_status=?, card_id=? WHERE vc_id=?', ('Available', 'N/A', VC_id))
       connector.commit()
    else: 
        mb.showinfo('Cannot be returned', 'The vaccine status cannot be set to Available unless it has been returned')  
        cursor.execute('UPDATE Library SET vc_status=?, card_id=? where vc_id=?', ('Issued', issuer_card(), VC_id))
    connector.commit()
    clear_and_display()

def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')
    if not Cid:
     mb.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
    else:
      return Cid
    
def display_records():
    global connector, cursor
    global tree
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)

def clear_fields():
    global vc_status, vc_id, vc_name, company_name, card_id
    vc_status.set('Available')
    for i in ['vc_id', 'vc_name', 'company_name', 'card_id']:
     exec(f"{i}.set('')")
     vc_id_entry.config(state='normal')
    try:
      tree.selection_remove(tree.selection()[0])
    except:
           pass
    
def clear_and_display():
     clear_fields()
     display_records()

def view_record():
         global vc_name, vc_id, vc_status, company_name, card_id
         global tree
         if not tree.focus():
           mb.showerror('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
           return
         current_item_selected = tree.focus()
         values_in_selected_item = tree.item(current_item_selected)
         selection = values_in_selected_item['values']
         vc_name.set(selection[0]) ; vc_id.set(selection[1]) ; vc_status.set(selection[3])
         company_name.set(selection[2])

root.update()
root.mainloop()