import tkinter as tk


class HighpassGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Highpass")

        # Label Creation
        self.input_lbl = tk.Label(
            self, text="Enter Highpass output below:", font=('calibri', 12))
        self.input_lbl.grid(row=0, column=0, padx=50, pady=5)

        # TextBox Creation
        self.input_txt = tk.Text(self,
                                 height=20,
                                 width=50)
        self.input_txt.grid(row=1, column=0, padx=50, pady=10)

        # Button Creation
        self.print_button = tk.Button(self,
                                      text="Print",
                                      command=self.parse_input)
        self.print_button.grid(row=2, column=0, padx=50, pady=10)

        # Label
        self.lbl = tk.Label(self, text="")
        self.lbl.grid(row=3, column=0, padx=50, pady=10)

    def parse_input(self):
        inp = self.input_txt.get(1.0, "end-1c")
        self.lbl.config(text="Provided Input: "+inp)

    def run(self):
        self.mainloop()
        
gui = HighpassGUI()
gui.run()