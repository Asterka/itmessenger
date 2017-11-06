import socket
import names
from tkinter import *
from PIL import ImageTk as imgtk
from PIL import Image as img



tk=Tk()



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12344));
my_name = names.get_first_name()
sock.sendto (("0 "+ my_name).encode(),('127.0.0.1',5555))

text=StringVar()
name=StringVar()

name.set(my_name)
text.set('')
tk.title('Chat')
tk.geometry('400x300')

log = Text(tk)
nick = Entry(tk, textvariable=name)
msg = Entry(tk, textvariable=text)

msg.pack(side='bottom', fill='x', expand='true')
nick.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both',expand='true')
def hi(event):
   log.see(END)
   log.insert(END,"hi")
def loopproc():
  log.see(END)
  sock.setblocking(False)
  try:
    message = sock.recv(128).decode()
    print(message)
    user = message.split()[0]
    message = message[len(user):]
    log.insert(END,user + ": "+ message + '\n')
  except:
    tk.after(1,loopproc)
    return
  tk.after(1,loopproc)
  return

def sendproc(event):
  sock.sendto (("1 "+''.join(name.get().split())+' '+text.get()).encode(),('127.0.0.1',5555))
  text.set('')

myimg = img.open('test.gif')
myimg = myimg.resize((100, 100), img.ANTIALIAS)
newImg = imgtk.PhotoImage(myimg)
content = Label(tk, image=newImg)
#content.place(x=0, y=0);
msg.bind('<Return>',sendproc)
msg.bind('z',hi)
msg.focus_set()

tk.after(1,loopproc)
tk.mainloop()
