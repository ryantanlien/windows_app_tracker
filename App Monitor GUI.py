from tkinter import *
import database

#Things to do:
# Enable a drop down menu to change the listbox from process name to App Name
# Enable a sorting function for the listbox

def get_raw_list():
    conn = database.create_connecton('database.db')
    raw_list = database.get_all(conn)
    return raw_list

def show_cur_selection(*args):
    index = process_listbox.curselection() #Returns a list of the index of all selected elements in the listbox
    process_timeused = StringVar(value = raw_list[index[0]][4])
    process_timeused_label['textvariable'] = process_timeused
    process_appname = StringVar(value = raw_list[index[0]][2])
    process_appname_label['textvariable'] = process_appname
    process_exe = StringVar(value = raw_list[index[0]][1])
    process_exe_label['textvariable'] = process_exe

root = Tk()
root.title("App Monitor")
root.option_add('*tearOff', FALSE)

#Creates a menu in top level window
menubar = Menu(root)
root['menu'] = menubar

#Adding menus to the menubar
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu = menu_file, label = 'File')
menubar.add_cascade(menu = menu_edit, label = 'Edit')
menu_file.add_command(label = 'New',)
menu_file.add_command(label = 'Open...',)
menu_file.add_command(label = 'Close',)
menu_file.add_separator()
menu_file.add_cascade(label = 'Exit')

#Listbox management
process_name_list = []
raw_list = get_raw_list()
if len(raw_list) != 0:
    for process in raw_list:
        process_name_list.append(process[1])
listnames = StringVar(value = process_name_list)
process_listbox = Listbox(root, height = 10)
process_listbox['listvariable'] = listnames
process_listbox['selectmode'] = "browse"
process_listbox.grid(column = 1, row = 1, columnspan = 2)
process_listbox.bind('<<ListboxSelect>>', show_cur_selection)

#Label under listbox
timeused_label = Label(root, text = "Time Used:")
timeused_label.grid(column = 1, row = 2)
process_timeused_label = Label(root)
process_timeused_label.grid(column = 2, row = 2)

exe_label = Label(root, text = "App Exe Name:")
exe_label.grid(column = 1, row = 4)
process_exe_label = Label(root)
process_exe_label.grid(column = 2, row = 4)

appname_label = Label(root, text = "App Name:")
appname_label.grid(column = 1, row = 3)
process_appname_label = Label(root)
process_appname_label.grid(column = 2, row = 3)
root.mainloop()
