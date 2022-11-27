import tkinter as tk

frame = tk.Tk()
frame.title("TextBox Input")


def printInput():
    inp = input_txt.get(1.0, "end-1c")
    lbl.config(text="Provided Input: "+inp)


# TextBox Creation

input_lbl = tk.Label(
    frame, text="Enter Highpass output below:", font=('calibri', 12))
input_lbl.grid(row=0, column=0, padx=50, pady=5)

input_txt = tk.Text(frame,
                    height=20,
                    width=50)
input_txt.grid(row=1, column=0, padx=50, pady=10)

# Button Creation
printButton = tk.Button(frame,
                        text="Print",
                        command=printInput)

# Label Creation
lbl = tk.Label(frame, text="")
frame.mainloop()
