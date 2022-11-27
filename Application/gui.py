import tkinter as tk

frame = tk.Tk()
frame.title("TextBox Input")


def parse_input():
    inp = input_txt.get(1.0, "end-1c")
    tk.Message(frame, text=inp).grid(row=3, column=0, padx=50, pady=10)


# TextBox Creation

input_lbl = tk.Label(
    frame, text="Enter Highpass output below:", font=('calibri', 12))
input_lbl.grid(row=0, column=0, padx=50, pady=5)

input_txt = tk.Text(frame,
                    height=20,
                    width=50)
input_txt.grid(row=1, column=0, padx=50, pady=10)

# Button Creation
parse_btn = tk.Button(frame,
                        text="Print",
                        command=parse_input)
parse_btn.grid(row=2, column=0, padx=20, pady=10)

# Label Creation
lbl = tk.Label(frame, text="")
frame.mainloop()
