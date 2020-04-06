import socket
from tkinter import *
from tkinter.ttk import *
from threading import *

#To terminate thread
flag = True

#Send msgs and update message list
def reader():
    msg = box.get()
    msg_lst.insert(END, f'|->: {msg}')
    c.send(bytes(msg, 'utf-8'))

#Close connection and disable buttons
def end_conn(var):
    global flag
    if var == 0:
        c.send(bytes(':END IT:', 'utf-8'))
    flag = False
    c.close()
    read.config(state=DISABLED)
    end.config(state=DISABLED)

#To check and read msgs from client
def msg_updater():
    global flag
    while flag:
        msg_read = c.recv(1024).decode()
        if msg_read:
            msg_lst.insert(END, f'{client_name}: {msg_read}')
        if msg_read == ":END IT:":
            end_conn(1)


#Thread for message update
t1 = Thread(target=msg_updater)

#GUI
window = Tk()
window.title('Chatbox')
heading = Label(window,text='Chatbox:: |->',width=35).grid(row=1,column=0)
box = Entry(window,width=40)
box.grid(row=2,column=0)
read = Button(window,text='Send',command=reader)
read.grid(row=2,column=1)
main_frame = LabelFrame(window)
main_frame.grid(row=0,column=0)
msg_scroll = Scrollbar(main_frame,orient="horizontal")
msg_scroll.pack(side=BOTTOM,fill=X)
msg_lst = Listbox(main_frame,width=60)
msg_lst.pack()
msg_lst.config(xscrollcommand=msg_scroll.set)
msg_scroll.config(command=msg_lst.xview)

#Socket setup
s = socket.socket()
s.bind(('localhost',11111))
s.listen(5)
print("Socket with port:11111 Initiated")

c, port = s.accept()
name = input('Enter Client name : ')
c.send(bytes(name,'utf-8'))
client_name = c.recv(1024).decode()

print(f'Connected with {client_name} at 11111')
Conn_info = Label(window,text=f'Logged in as {name}\n\nConnected to {client_name}').grid(row=0,column=1)
c.send(bytes('Connected to the Server','utf-8'))

end = Button(window,text='End Connection',command=lambda : end_conn(0))
end.grid(row=1,column=1)

t1.start()
window.mainloop()
