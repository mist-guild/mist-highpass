import tkinter as tk
from tkinter import messagebox
from parse import Parser, resource_path
import datetime


class HighpassGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Highpass")
        self.iconphoto(False, tk.PhotoImage(
            file=resource_path('./assets/logo.png')))
        self.resizable(False, False)

        self.parser = Parser()

        # Parse Label Creation
        self.input_lbl = tk.Label(
            self, text="Enter Highpass output below:", font=('calibri', 12))
        self.input_lbl.grid(row=0, column=0, padx=50, pady=5)

        # Parse TextBox Creation
        self.input_txt = tk.Text(self,
                                 height=20,
                                 width=50)
        self.input_txt.grid(row=1, column=0, padx=50, pady=10)

        # Check Headers Button Creation
        self.headers_btn = tk.Button(self,
                                     text="Check headers",
                                     bg="coral",
                                     font=('calibri', 12),
                                     command=self.check_headers)
        self.headers_btn.grid(row=2, column=0, padx=50, pady=5, sticky="nesw")

        # Parse Button Creation
        self.parse_btn = tk.Button(self,
                                   text="Parse",
                                   bg="lightblue",
                                   font=('calibri', 12),
                                   command=self.parse)
        self.parse_btn.grid(row=3, column=0, padx=50, pady=5, sticky="nesw")

    def __save_input(self, input):
        lines = input.splitlines()
        e = datetime.datetime.now()
        with open(f'{e.strftime("%Y-%m-%d-%H-%M-%S")}.txt', 'w') as f:
            for line in lines:
                f.write(line + "\n")

    def check_headers(self):
        # validate input
        input = self.input_txt.get("1.0", "end-1c")
        result, violation = self.parser.validate_input(input)
        if result == False:
            messagebox.showerror(
                'Highpass Error', 'Parsing failed! Your input is invalid. Violated line: ' + violation)
            return
        messagebox.showinfo(
            "Highpass Success", "Input is valid! Checking headers...")

        missed = self.parser.check_missing_headers(input)
        if missed == True:
            messagebox.showinfo(
                "Highpass Success", "Missed headers found! Please check missed_headers.txt.")
        else:
            messagebox.showinfo("Highpass Success", "No missed headers found!")

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
        self.__save_input(input)

    def run(self):
        self.mainloop()
