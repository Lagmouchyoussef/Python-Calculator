import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.memory = 0
        
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        """Creates the display area"""
        display_frame = tk.Frame(self.root, bg='#2C2C2C')
        display_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 18),
            justify='right',
            state='readonly',
            bg='#2C2C2C',
            fg='white',
            bd=0
        )
        self.display.pack(fill=tk.X, ipady=10)
    
    def create_buttons(self):
        """Creates calculator buttons"""
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        buttons = [
            ['MC', 'MR', 'M+', 'M-', 'C'],
            ['√', 'x²', '1/x', '±', '←'],
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', '=', '+', 'π']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                button = tk.Button(
                    buttons_frame,
                    text=text,
                    font=('Arial', 12),
                    command=lambda t=text: self.button_click(t),
                    bg=self.get_button_color(text),
                    fg='white',
                    bd=0,
                    relief='flat'
                )
                button.grid(
                    row=i, column=j, 
                    sticky='nsew', 
                    padx=2, pady=2,
                    ipadx=10, ipady=10
                )
        
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def get_button_color(self, text):
        """Returns button color based on its function"""
        if text in ['=', 'C', '←']:
            return '#FF9500'
        elif text in ['MC', 'MR', 'M+', 'M-']:
            return '#505050'
        elif text in ['√', 'x²', '1/x', '±', 'sin', 'cos', 'tan', 'π']:
            return '#505050'
        elif text in ['/', '*', '-', '+']:
            return '#FF9500'
        else:
            return '#666666'
    
    def button_click(self, text):
        """Handles button clicks"""
        try:
            if text.isdigit() or text == '.':
                self.input_number(text)
            elif text in ['+', '-', '*', '/']:
                self.input_operator(text)
            elif text == '=':
                self.calculate()
            elif text == 'C':
                self.clear()
            elif text == '←':
                self.backspace()
            elif text == '±':
                self.negate()
            elif text == '√':
                self.square_root()
            elif text == 'x²':
                self.square()
            elif text == '1/x':
                self.reciprocal()
            elif text in ['sin', 'cos', 'tan']:
                self.trig_function(text)
            elif text == 'π':
                self.input_pi()
            elif text in ['MC', 'MR', 'M+', 'M-']:
                self.memory_operation(text)
        except Exception as e:
            self.display_error()
    
    def input_number(self, num):
        """Adds a digit or decimal point"""
        if self.current_input == "0" or self.current_input == "Error":
            self.current_input = ""
        
        if num == '.' and '.' in self.current_input:
            return  
        
        self.current_input += num
        self.result_var.set(self.current_input)
    
    def input_operator(self, op):
        """Adds an operator"""
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/']:
            self.current_input += op
            self.result_var.set(self.current_input)
    
    def calculate(self):
        """Performs the calculation"""
        try:
            if self.current_input:
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.current_input = str(result)
                self.result_var.set(self.current_input)
        except:
            self.display_error()
    
    def clear(self):
        """Clears everything"""
        self.current_input = ""
        self.result_var.set("0")
    
    def backspace(self):
        """Deletes the last character"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else "0")
    
    def negate(self):
        """Changes the sign"""
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_var.set(self.current_input)
    
    def square_root(self):
        """Calculates square root"""
        try:
            result = math.sqrt(float(self.current_input))
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except:
            self.display_error()
    
    def square(self):
        """Calculates square"""
        try:
            result = float(self.current_input) ** 2
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except:
            self.display_error()
    
    def reciprocal(self):
        """Calculates reciprocal"""
        try:
            result = 1 / float(self.current_input)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except:
            self.display_error()
    
    def trig_function(self, func):
        """Calculates trigonometric functions"""
        try:
            angle = float(self.current_input)
            if func == 'sin':
                result = math.sin(math.radians(angle))
            elif func == 'cos':
                result = math.cos(math.radians(angle))
            elif func == 'tan':
                result = math.tan(math.radians(angle))
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except:
            self.display_error()
    
    def input_pi(self):
        """Inserts pi value"""
        self.current_input = str(math.pi)
        self.result_var.set(self.current_input)
    
    def memory_operation(self, op):
        """Handles memory operations"""
        try:
            current_value = float(self.current_input) if self.current_input else 0
            
            if op == 'MC':  
                self.memory = 0
            elif op == 'MR':  
                self.current_input = str(self.memory)
                self.result_var.set(self.current_input)
            elif op == 'M+':  
                self.memory += current_value
            elif op == 'M-':  
                self.memory -= current_value
        except:
            self.display_error()
    
    def display_error(self):
        """Displays error message"""
        self.current_input = ""
        self.result_var.set("Error")

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()