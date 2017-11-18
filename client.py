import socket
import names
from Tkinter import *
from PIL import ImageTk as imgtk
from PIL import Image as img
import tkFileDialog
import ttk
import os
import time


tk=Tk()
tk.geometry("400x300")
m = Menu(tk)

tk.config(menu=m)


enc = 1
com = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12344));
my_name = names.get_first_name()
sock.sendto (b'0000'+(my_name).encode(),('127.0.0.1',12344))
width, height = tk.winfo_screenwidth(), tk.winfo_screenheight()

text=StringVar()
name=StringVar()
downloadButtons = []
name.set(my_name)
text.set('')
tk.title('Chat')

myimg = img.open('fon.bmp')
btnimg = img.open('btn2.png')
sf = img.open('send_file.png')

myimg = myimg.resize((width, height), img.ANTIALIAS)
sf = sf.resize((50, 50))
btnimg = btnimg.resize((50, 50))

backImg = imgtk.PhotoImage(myimg)
btnImg = imgtk.PhotoImage(btnimg)
sfImg = imgtk.PhotoImage(sf)

content = Label(tk, image=backImg)

b = Button(tk, text="My Text", image=backImg, relief="flat", state="disabled")
b.place(x =0, y =0)

l = Text(tk, height = 20, width = 100)
l.grid(column=0, row=0, sticky=(N,W,E,S))


s = Scrollbar(tk, orient=VERTICAL, command=l.yview)
s.grid(column=1, row=0, sticky=(N,S))
l['yscrollcommand'] = s.set

ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))
tk.grid_columnconfigure(0, weight=1)
tk.grid_rowconfigure(0, weight=1)

nick = Entry(tk,width = 15, textvariable=name)
msg = Entry(tk, width = width,textvariable=text)
msg.grid(sticky = (S,E))
nick.grid(sticky=(S))


isBusy =  False


class myButton(Button):
        id = ""

def set_encoding(num):
        global enc
        enc = num
        
def set_compression(num):
        global com
        com = num
        
def write_line(str):
        l.config(state=NORMAL)
        l.insert('end',str)
        l.config(state=DISABLED)


def load_file_from_server(self):
        print(self.widget.id)
        sock.setblocking(True)
        if isBusy == False:
                #send file
                sock.sendto (b'0111' + (" " + self.widget.id).encode(), ('127.0.0.1',12344))
                data = sock.recv(4)
                if data[0:4] == b"1000":
                        write_line("File you requested is not on the server" + '\n')
                else:
                        rec = True
                        while rec:
                                res = sock.recv(1)
                                if res.decode() != " ":
                                        data = data + res
                                else:
                                        rec = False
                                        break
                        size = data[4:].decode()
                        print(size)
                        buffer = []
                        while len(buffer) < int(size):
                                buffer += sock.recv(4096)
                        print(len(buffer))
                        directory = tkFileDialog.askdirectory()
                        file_name = "Cli"+self.widget.id
                        f = open(directory+"/"+file_name, 'wb')
                        f.write(bytes(buffer))
                        f.close()
                        write_line("File "+ file_name + " has been uploaded into " + directory + '\n')
                        
          
        else:
           write_line("Sorry, you cannnot downloads files while uploading one" + '\n')
        sock.setblocking(False)


def load_file():
        fname = tkFileDialog.askopenfilename()
        if fname:
                send_file(None, fname)


def loopproc():
  sock.setblocking(False)
  try:
    data = sock.recv(128)
    #add message type check here
    opcode = data[0:4]
    #print(opcode)
    message = ""
    user = ""
    message = data[4:].decode()
    user = message.split()[0]
    global isBusy
    #connected/disconnected users
    
    if opcode == b"0000":
        write_line(user + " has connected to the network" + '\n')
      
    if opcode == b"0011":
        write_line(user + " has disconnected from the network" + '\n')
    #----------------------------
    if opcode == b"0001":
        write_line(user + ": "+ message[len(user)+2:] + '\n')
      
    if opcode == b"0100":
        write_line(user + " is now sending a file" + '\n')
        
    if opcode == b"0101":
      isBusy = False
      butt_id = message.split()[1]
      btn = myButton(tk ,text="File", width=15)
      btn.id = butt_id
      btn.bind('<Button-1>', load_file_from_server);
      write_line(user + " has sent a file" + '\n')
      l.window_create('end', window=btn)
      write_line("\n")
      
      #downloadButtons.append(btn)
  except:
    tk.after(1,loopproc)
    return
  tk.after(1,loopproc)
  return


def send_text(event):
  my_name = name.get()
  if text.get() != "":
          global isBusy
          if isBusy == False:
                sock.sendto (b'0001'+(my_name+' '+text.get()).encode(),('127.0.0.1',12344))
          else:
             write_line("Sorry, you cannnot send messages while file is being sent or uploaded" + '\n')   
          text.set('')


def send_file(event, filepath):
  sock.setblocking(True)      
  if isBusy == False:
          buffer = []
          filename, file_extension = os.path.splitext(filepath)
          send_name = filepath.split('/')[-1]
          f = open(filepath, "rb")
          buffer = f.read()
          #print(len(buffer))
          f.close()
          sock.sendto (b'0010'+(file_extension + str(len(buffer))).encode(),('127.0.0.1',12344))
          time.sleep(0.2)
          try:
                  sock.sendto (buffer, ('127.0.0.1',12344))
          except:
                  print("exception occured")
  else:
           write_line("Sorry, you cannnot send files while another file is being sent" + '\n')

#myimg = img.open('test.gif')
#myimg = myimg.resize((100, 100), img.ANTIALIAS)
#newImg = imgtk.PhotoImage(myimg)
#l.image_create('end',image=newImg)


msg.bind('<Return>',send_text)
msg.focus_set()

btn_send_file = Button(tk ,text="Browse", command= load_file,  image= sfImg)
btn_send_message = Button(tk ,text="Send Message", command= send_text, image= btnImg)
btn_send_file.grid(sticky = (S,E))
btn_send_message.grid(sticky = (S,E))
btn_send_message.bind('<Button-1>', send_text)

encoding = Menu(m)

m.add_cascade(label="Encoding",menu=encoding)
num = 1
encoding.add_command(label="1.Hamming",command = lambda *num: set_encoding(1))
encoding.add_command(label="2.Repetition",command = lambda *num: set_encoding(2))
encoding.add_command(label="3.Parity",command =lambda *num: set_encoding(3))
encoding.add_command(label="4.CRC",command =lambda *num: set_encoding(4))

compression = Menu(m)
m.add_cascade(label="Compression",menu=compression)
compression.add_command(label="1.Huffman",command = lambda *num: set_compression(1))
compression.add_command(label="2.LZ78",command = lambda *num: set_compression(2))
compression.add_command(label="3.Shannon-Fano",command =  lambda *num: set_compression(3))


tk.after(1,loopproc)
tk.mainloop()
