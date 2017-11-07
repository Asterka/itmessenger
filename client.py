import socket
import names
from tkinter import *
from tkinter import ttk
from PIL import ImageTk as imgtk
from PIL import Image as img
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import ttk

tk=Tk()



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12344));
my_name = names.get_first_name()
sock.sendto (("0 "+ my_name).encode(),('127.0.0.1',12344))

text=StringVar()
name=StringVar()

name.set(my_name)
text.set('')
tk.title('Chat')

l = Listbox(tk, height = 10, width = 100)
l.grid(column=0, row=0, sticky=(N,W,E,S))
s = Scrollbar(tk, orient=VERTICAL, command=l.yview)
s.grid(column=1, row=0, sticky=(N,S))
l['yscrollcommand'] = s.set

ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))
tk.grid_columnconfigure(0, weight=1)
tk.grid_rowconfigure(0, weight=1)

nick = Label(tk, textvariable=name)
msg = Entry(tk, width = 100,textvariable=text)

msg.grid(sticky = (S,E))
nick.grid(sticky=(S))

def load_file():
        fname = askopenfilename()
        if fname:
            try:
                print("You want to open "+ fname+ "file")
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
         
def loopproc():
  sock.setblocking(False)
  try:
    message = sock.recv(128).decode()
    user = message.split()[0]
    l.insert('end',user + ": "+ message[len(user):] + '\n')
  except:
    tk.after(1,loopproc)
    return
  tk.after(1,loopproc)
  return

def sendproc(event):
  sock.sendto (("1 "+ my_name+' '+text.get()).encode(),('127.0.0.1',12344))
  text.set('')
  

#myimg = img.open('test.gif')
#myimg = myimg.resize((100, 100), img.ANTIALIAS)
#newImg = imgtk.PhotoImage(myimg)
#content = Label(tk, image=newImg)
#content.place(x=0, y=0);

btn_send_file = Button(tk ,text="Browse", command= load_file, width=15)
btn_send_message = Button(tk ,text="Send Message", command= sendproc, width=15)
msg.bind('<Return>',sendproc)
msg.focus_set()
btn_send_file.grid(sticky = (S,E))
btn_send_message.grid(sticky = (S,E))
btn_send_message.bind('<Button-1>', sendproc);
tk.after(1,loopproc)
tk.mainloop()
