import tkinter as tk
from tkinter import messagebox
from parse import Parser, resource_path


class HighpassGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Highpass")
        self.iconphoto(False, tk.PhotoImage(
            file=resource_path('./assets/logo.png')))
        self.resizable(False, False)

        self.parser = Parser()

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
        self.parse_btn = tk.Button(self,
                                   text="Parse",
                                   bg="lightblue",
                                   font=('calibri', 12),
                                   command=self.parse)
        self.parse_btn.grid(row=2, column=0, padx=50, pady=5, sticky="nesw")

    def parse(self):
        # validate input
        input = self.input_txt.get("1.0", "end-1c")
        result, violation = self.parser.validate_input(input)
        if result == False:
            messagebox.showerror(
                'Highpass Error', 'Parsing failed! Your input is invalid. Violated line: ' + violation)
            return
        messagebox.showinfo(
            "Highpass Success", "Input is valid! Highpass will begin parsing...")

        # parse input
        self.parser.parse(input)

        # confirmation
        messagebox.showinfo(
            "Highpass Success", "Parsing complete! Reagent counts have been published to both Valdrakken and the Google Sheet.")

    def run(self):
        self.mainloop()
