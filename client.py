import socket
import names
from tkinter import *
from tkinter import ttk
from PIL import ImageTk as imgtk
from PIL import Image as img
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import ttk
import os

tk=Tk()



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12344));
my_name = names.get_first_name()
sock.sendto (b'0000'+(my_name).encode(),('127.0.0.1',12344))

text=StringVar()
name=StringVar()
downloadButtons = []
name.set(my_name)
text.set('')
tk.title('Chat')

l = Text(tk, height = 20, width = 100)
l.grid(column=0,
       row=0, sticky=(N,W,E,S))

s = Scrollbar(tk, orient=VERTICAL, command=l.yview)
s.grid(column=1, row=0, sticky=(N,S))
l['yscrollcommand'] = s.set

ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))
tk.grid_columnconfigure(0, weight=1)
tk.grid_rowconfigure(0, weight=1)

nick = Entry(tk,width = 15, textvariable=name)
msg = Entry(tk, width = 100,textvariable=text)
msg.grid(sticky = (S,E))
nick.grid(sticky=(S))

def load_file_from_server():
        print("Try to load")
        pass
def load_file():
        fname = askopenfilename()
        if fname:
                send_file(None, fname)
def loopproc():
  sock.setblocking(False)
  try:
    data = sock.recv(128)
    #add message type check here
    opcode = data[0:4]
    print(str(opcode))
    message = ""
    user = ""
    if opcode != b"0100":
        message = data[4:].decode()
        user = message.split()[0]
        
    #connected/disconnected users
    if opcode == b"0000":
      l.insert('end',user + " has connected to the network" + '\n')
      
    if opcode == b"0011":
      l.insert('end',user + " has disconnected from the network" + '\n')
    #----------------------------
    if opcode == b"0001":
      print("here")
      l.insert('end',user + ": "+ message[len(user)+2:] + '\n')
      
    if opcode == b"0010":
      btn = Button(tk ,text="File", command = load_file_from_server, width=15)
      l.insert('end',"File has been uploaded")
      l.window_create('end', window=btn)
      l.insert('end',"\n")
      
      #downloadButtons.append(btn)
  except:
    tk.after(1,loopproc)
    return
  tk.after(1,loopproc)
  return

def send_text(event):
  my_name = name.get()
  sock.sendto (b'0001'+(my_name+' '+text.get()).encode(),('127.0.0.1',12344))
  text.set('')
def send_file(event, filepath):
  filename, file_extension = os.path.splitext(filepath)
  send_name = filepath.split('/')[-1]
  f = open(filepath, "rb")
  buffer = f.read()
  f.close()
  sock.sendto (b'0010'+(file_extension).encode(),('127.0.0.1',12344))
  sock.sendto(b'0100' + bytes(len(buffer)),('127.0.0.1',12344))
  sock.sendto(buffer ,('127.0.0.1',12344))

#myimg = img.open('test.gif')
#myimg = myimg.resize((100, 100), img.ANTIALIAS)
#newImg = imgtk.PhotoImage(myimg)
#l.image_create('end',image=newImg)


msg.bind('<Return>',send_text)
msg.focus_set()

btn_send_file = Button(tk ,text="Browse", command= load_file, width=15)
btn_send_message = Button(tk ,text="Send Message", command= send_text, width=15)
btn_send_file.grid(sticky = (S,E))
btn_send_message.grid(sticky = (S,E))
btn_send_message.bind('<Button-1>', send_text);

tk.after(1,loopproc)
tk.mainloop()
