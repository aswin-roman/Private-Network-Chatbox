import socket
from tkinter import *
from tkinter.ttk import *
from threading import *

flag = True

def reader():
    msg = box.get()
    tree.insert('', 'end', text=f'|->: {msg}')
    c.send(bytes(msg,'utf-8'))

def end_conn(var):
    global flag
    if var == 0:
        c.send(bytes(':END IT:', 'utf-8'))
    flag = False
    c.close()
    read.config(state=DISABLED)
    end.config(state=DISABLED)

def msg_updater():
    global flag
    while flag:
        msg_read = c.recv(1024).decode()
        if msg_read:
            tree.insert('', 'end', text=f'{client_name}: {msg_read}')
        if msg_read == ':END IT:':
            end_conn(1)


t1 = Thread(target=msg_updater)
window = Tk()
window.title('Chatbox')
heading = Label(window,text='Chatbox',width=35).grid(row=1,column=0)
box = Entry(window)
box.grid(row=2,column=0)
read = Button(window,text='Send',command=reader)
read.grid(row=2,column=1)
tree = Treeview(window)
tree.grid(row=0,column=0)

s = socket.socket()
s.bind(('localhost',11111))
s.listen(5)
print("Socket with port:11111 Initiated")

c, port = s.accept()
name = input('Enter Client name : ')
c.send(bytes(name,'utf-8'))
client_name = c.recv(1024).decode()

print(f'Connected with {client_name} at {port}')
Conn_info = Label(window,text=f'Logged in as {name}\n\nConnected to {client_name}').grid(row=0,column=1)
c.send(bytes('Connected to the Server','utf-8'))

end = Button(window,text='End Connection',command=lambda: end_conn(0))
end.grid(row=1,column=1)

t1.start()
window.mainloop()
