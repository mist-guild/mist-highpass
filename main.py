
from tkinter import *
import tkinter.scrolledtext as tkscrolled

root = Tk()
root.geometry("700x600")
root.title(" Highpass - Mist Guild ")
root.configure(background='white')


title_lbl = Label(text="Insert Highpass WoW Addon Input",
                  font=("Calibri", 25),
                  pady=10,
                  background='white')

input_txt = tkscrolled.ScrolledText(root,
                                    font=("Calibri", 10),
                                    height=30,
                                    width=50,
                                    bg="light yellow")

send_btn = Button(root,
                  height=3,
                  width=20,
                  text="Waiting for input...",
                  bg="light blue",
                  state=DISABLED)

title_lbl.pack()
input_txt.pack()
send_btn.pack(pady=10)
mainloop()
