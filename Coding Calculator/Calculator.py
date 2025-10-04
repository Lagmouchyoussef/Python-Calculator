import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
import math
import random
import json
import time

class QuantumCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Calculator ∞ Pro (Light)")
        self.root.geometry("900x650")
        self.root.configure(bg='#0a0a0a')
        
        # Variables d'état
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.memory = 0
        self.history = []
        self.theme_colors = {
            'bg': '#0a0a0a',
            'display_bg': '#001122',
            'display_fg': '#00ffcc',
            'button_bg': '#004466',
            'button_fg': 'white',
            'operator_bg': '#0066cc',
            'special_bg': '#cc3300',
            'scientific_bg': '#003366'
        }
        self.angle_mode = 'deg'  # 'deg' or 'rad'
        self.fullscreen = False
        
        # Initialisation
        self.setup_styles()
        self.create_interface()
        self.setup_keyboard_shortcuts()
        self.load_settings()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.update_styles()
        
    def update_styles(self):
        self.style.configure('Futuristic.TFrame', background=self.theme_colors['bg'])
        self.style.configure('Display.TEntry', 
                           fieldbackground=self.theme_colors['display_bg'], 
                           foreground=self.theme_colors['display_fg'], 
                           font=('Courier', 20, 'bold'))
        
        self.style.configure('SciButton.TButton',
                           font=('Arial', 10),
                           background=self.theme_colors['scientific_bg'],
                           foreground=self.theme_colors['button_fg'],
                           borderwidth=1)
        
        self.style.configure('NumButton.TButton',
                           font=('Arial', 12, 'bold'),
                           background=self.theme_colors['button_bg'],
                           foreground=self.theme_colors['button_fg'])
        
        self.style.configure('OpButton.TButton',
                           font=('Arial', 12, 'bold'),
                           background=self.theme_colors['operator_bg'],
                           foreground=self.theme_colors['button_fg'])
        
        self.style.configure('Special.TButton',
                           font=('Arial', 11, 'bold'),
                           background=self.theme_colors['special_bg'],
                           foreground=self.theme_colors['button_fg'])
        
        # Style pour les onglets
        self.style.configure('TNotebook', background=self.theme_colors['bg'])
        self.style.configure('TNotebook.Tab', background=self.theme_colors['button_bg'], 
                           foreground=self.theme_colors['button_fg'])
        self.style.map('TNotebook.Tab', background=[('selected', self.theme_colors['operator_bg'])])

    def create_interface(self):
        # Barre de menu
        self.create_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Futuristic.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panneau supérieur avec affichage et contrôles
        top_frame = ttk.Frame(main_frame, style='Futuristic.TFrame')
        top_frame.pack(fill=tk.X, pady=(0,10))
        
        self.create_display(top_frame)
        self.create_controls(top_frame)
        
        # Panneau inférieur avec onglets
        self.create_tabs(main_frame)
        
        # Barre de status
        self.create_status_bar()
    
    def create_menu(self):
        menubar = tk.Menu(self.root, bg='#0a0a0a', fg='white')
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0, bg='#0a0a0a', fg='white')
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_calculation)
        file_menu.add_command(label="Ouvrir", command=self.load_calculation)
        file_menu.add_command(label="Sauvegarder", command=self.save_calculation)
        file_menu.add_separator()
        file_menu.add_command(label="Exporter l'historique", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0, bg='#0a0a0a', fg='white')
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Copier", command=self.copy_result, accelerator="Ctrl+C")
        edit_menu.add_command(label="Coller", command=self.paste_input, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Préférences", command=self.open_preferences)
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0, bg='#0a0a0a', fg='white')
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Plein écran", command=self.toggle_fullscreen, accelerator="F11")
        view_menu.add_command(label="Thème", command=self.change_theme)
        view_menu.add_checkbutton(label="Mode angle: Degrés", command=self.toggle_angle_mode)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0, bg='#0a0a0a', fg='white')
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="Manuel d'utilisation", command=self.show_help)
        help_menu.add_command(label="À propos", command=self.show_about)
    
    def create_display(self, parent):
        display_frame = ttk.Frame(parent, style='Futuristic.TFrame')
        display_frame.pack(fill=tk.X, pady=(0,5))
        
        # Affichage de l'expression en cours
        self.expression_var = tk.StringVar()
        self.expression_var.set("")
        self.expression_display = ttk.Entry(display_frame, 
                                         textvariable=self.expression_var,
                                         style='Display.TEntry',
                                         justify='right',
                                         font=('Courier', 14))
        self.expression_display.pack(fill=tk.X, ipady=5)
        
        # Affichage du résultat
        self.display = ttk.Entry(display_frame, 
                               textvariable=self.result_var,
                               style='Display.TEntry',
                               justify='right',
                               state='readonly')
        self.display.pack(fill=tk.X, ipady=12)
    
    def create_controls(self, parent):
        controls_frame = ttk.Frame(parent, style='Futuristic.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0,10))
        
        # Boutons de mémoire
        memory_frame = ttk.Frame(controls_frame, style='Futuristic.TFrame')
        memory_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(memory_frame, text="MC", style='Special.TButton', 
                  command=self.memory_clear).pack(side=tk.LEFT, padx=2)
        ttk.Button(memory_frame, text="MR", style='Special.TButton', 
                  command=self.memory_recall).pack(side=tk.LEFT, padx=2)
        ttk.Button(memory_frame, text="M+", style='Special.TButton', 
                  command=self.memory_add).pack(side=tk.LEFT, padx=2)
        ttk.Button(memory_frame, text="M-", style='Special.TButton', 
                  command=self.memory_subtract).pack(side=tk.LEFT, padx=2)
        
        # Indicateur de mode d'angle
        self.angle_indicator = ttk.Label(controls_frame, text=f"Mode: {self.angle_mode.upper()}", 
                                       foreground=self.theme_colors['display_fg'], 
                                       background=self.theme_colors['bg'])
        self.angle_indicator.pack(side=tk.RIGHT, padx=5)
        
        # Indicateur de mémoire
        self.memory_indicator = ttk.Label(controls_frame, text="M: 0", 
                                        foreground=self.theme_colors['display_fg'], 
                                        background=self.theme_colors['bg'])
        self.memory_indicator.pack(side=tk.RIGHT, padx=5)
    
    def create_tabs(self, parent):
        tab_control = ttk.Notebook(parent)
        
        # Onglets principaux
        basic_tab = ttk.Frame(tab_control)
        scientific_tab = ttk.Frame(tab_control)
        history_tab = ttk.Frame(tab_control)
        
        tab_control.add(basic_tab, text='Basic')
        tab_control.add(scientific_tab, text='Scientific')
        tab_control.add(history_tab, text='History')
        tab_control.pack(expand=True, fill=tk.BOTH)
        
        self.create_basic_tab(basic_tab)
        self.create_scientific_tab(scientific_tab)
        self.create_history_tab(history_tab)
    
    def create_basic_tab(self, parent):
        basic_frame = ttk.Frame(parent, style='Futuristic.TFrame')
        basic_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            ['C', '←', '(', ')', 'π', 'e'],
            ['7', '8', '9', '/', 'x²', '√'],
            ['4', '5', '6', '*', '1/x', '±'],
            ['1', '2', '3', '-', 'sin', 'cos'],
            ['0', '.', '=', '+', 'tan', 'log']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn_style = self.get_button_style(text)
                btn = ttk.Button(basic_frame, text=text, style=btn_style,
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2, ipadx=5, ipady=8)
                
                # Ajout d'effet de survol
                self.add_hover_effect(btn, text)
        
        for i in range(5):
            basic_frame.grid_rowconfigure(i, weight=1)
        for j in range(6):
            basic_frame.grid_columnconfigure(j, weight=1)
    
    def create_scientific_tab(self, parent):
        sci_frame = ttk.Frame(parent, style='Futuristic.TFrame')
        sci_frame.pack(fill=tk.BOTH, expand=True)
        
        sci_buttons = [
            ['sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'sinh', 'cosh', 'tanh'],
            ['log₁₀', 'log₂', 'ln', 'e^x', '2^x', '10^x'],
            ['x^y', 'n!', 'mod', '|x|', '⌊x⌋', '⌈x⌉'],
            ['deg→rad', 'rad→deg', 'P(n,r)', 'C(n,r)', 'gcd', 'lcm'],
            ['hex', 'bin', 'oct', 'rand', 'prime?', 'factor']
        ]
        
        for i, row in enumerate(sci_buttons):
            for j, text in enumerate(row):
                btn = ttk.Button(sci_frame, text=text, style='SciButton.TButton',
                               command=lambda t=text: self.scientific_click(t))
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2, ipadx=3, ipady=6)
                
                # Ajout d'effet de survol
                self.add_hover_effect(btn, text)
        
        for i in range(5):
            sci_frame.grid_rowconfigure(i, weight=1)
        for j in range(6):
            sci_frame.grid_columnconfigure(j, weight=1)

    def create_history_tab(self, parent):
        history_frame = ttk.Frame(parent, style='Futuristic.TFrame')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame pour les contrôles d'historique
        controls_frame = ttk.Frame(history_frame, style='Futuristic.TFrame')
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Effacer", style='Special.TButton',
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="Exporter", style='OpButton.TButton',
                  command=self.export_history).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="Importer", style='OpButton.TButton',
                  command=self.import_history).pack(side=tk.LEFT, padx=5)
        
        # Frame pour la liste d'historique
        list_frame = ttk.Frame(history_frame, style='Futuristic.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Création de la liste d'historique avec Treeview
        self.history_tree = ttk.Treeview(list_frame, columns=('Expression', 'Result'), 
                                        show='headings', height=15)
        self.history_tree.heading('Expression', text='Expression')
        self.history_tree.heading('Result', text='Résultat')
        self.history_tree.column('Expression', width=400)
        self.history_tree.column('Result', width=200)
        
        # Configuration des couleurs pour la Treeview
        self.history_tree.tag_configure('oddrow', background=self.theme_colors['display_bg'])
        self.history_tree.tag_configure('evenrow', background=self.theme_colors['button_bg'])
        
        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Liaison du double-clic pour réutiliser une expression
        self.history_tree.bind('<Double-1>', self.use_history_item)
    
    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, style='Futuristic.TFrame')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                    foreground=self.theme_colors['display_fg'], 
                                    background=self.theme_colors['bg'])
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Indicateur de calcul en cours
        self.calculation_indicator = ttk.Label(status_frame, text="", 
                                            foreground=self.theme_colors['display_fg'], 
                                            background=self.theme_colors['bg'])
        self.calculation_indicator.pack(side=tk.RIGHT, padx=5)
    
    def add_hover_effect(self, button, text):
        def on_enter(e):
            button_style = self.get_button_style(text)
            if button_style == 'NumButton.TButton':
                button.configure(background='#005577')
            elif button_style == 'OpButton.TButton':
                button.configure(background='#0077dd')
            elif button_style == 'Special.TButton':
                button.configure(background='#dd4400')
            elif button_style == 'SciButton.TButton':
                button.configure(background='#004477')
        
        def on_leave(e):
            button_style = self.get_button_style(text)
            if button_style == 'NumButton.TButton':
                button.configure(background=self.theme_colors['button_bg'])
            elif button_style == 'OpButton.TButton':
                button.configure(background=self.theme_colors['operator_bg'])
            elif button_style == 'Special.TButton':
                button.configure(background=self.theme_colors['special_bg'])
            elif button_style == 'SciButton.TButton':
                button.configure(background=self.theme_colors['scientific_bg'])
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def get_button_style(self, text):
        if text in ['C', '←']:
            return 'Special.TButton'
        elif text in ['+', '-', '*', '/', '=', 'mod']:
            return 'OpButton.TButton'
        elif text.isdigit() or text == '.':
            return 'NumButton.TButton'
        else:
            return 'SciButton.TButton'
    
    def setup_keyboard_shortcuts(self):
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-v>', lambda e: self.paste_input())
        self.root.bind('<Control-s>', lambda e: self.save_calculation())
        self.root.bind('<Control-o>', lambda e: self.load_calculation())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.button_click('←'))
        self.root.bind('<Key>', self.key_press)
    
    def key_press(self, event):
        if event.char.isdigit() or event.char in '+-*/.()':
            self.button_click(event.char)
        elif event.keysym == 'Delete':
            self.button_click('C')
    
    def button_click(self, text):
        try:
            if text.isdigit() or text == '.':
                self.input_number(text)
            elif text in ['+', '-', '*', '/', '(', ')', 'mod']:
                self.input_operator(text)
            elif text == '=':
                self.calculate_expression()
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
                self.input_constant('pi')
            elif text == 'e':
                self.input_constant('e')
            elif text == 'log':
                self.input_function('log10')
        except Exception as e:
            self.display_error(str(e))
    
    def scientific_click(self, text):
        try:
            if text == 'sin⁻¹':
                self.input_function('asin')
            elif text == 'cos⁻¹':
                self.input_function('acos')
            elif text == 'tan⁻¹':
                self.input_function('atan')
            elif text == 'sinh':
                self.input_function('sinh')
            elif text == 'cosh':
                self.input_function('cosh')
            elif text == 'tanh':
                self.input_function('tanh')
            elif text == 'log₁₀':
                self.input_function('log10')
            elif text == 'log₂':
                self.input_function('log2')
            elif text == 'ln':
                self.input_function('log')
            elif text == 'e^x':
                self.input_function('exp')
            elif text == '2^x':
                self.input_function('exp2')
            elif text == '10^x':
                self.input_operator('10**')
            elif text == 'x^y':
                self.input_operator('**')
            elif text == 'n!':
                self.factorial()
            elif text == 'mod':
                self.input_operator('%')
            elif text == '|x|':
                self.input_function('abs')
            elif text == '⌊x⌋':
                self.input_function('floor')
            elif text == '⌈x⌉':
                self.input_function('ceil')
            elif text == 'deg→rad':
                self.convert_deg_to_rad()
            elif text == 'rad→deg':
                self.convert_rad_to_deg()
            elif text == 'P(n,r)':
                self.permutation()
            elif text == 'C(n,r)':
                self.combination()
            elif text == 'gcd':
                self.input_function('gcd')
            elif text == 'lcm':
                self.input_function('lcm')
            elif text == 'hex':
                self.convert_base(16)
            elif text == 'bin':
                self.convert_base(2)
            elif text == 'oct':
                self.convert_base(8)
            elif text == 'rand':
                self.input_random()
            elif text == 'prime?':
                self.check_prime()
            elif text == 'factor':
                self.factorize()
        except Exception as e:
            self.display_error(str(e))
    
    def input_number(self, num):
        if self.current_input == "0" or self.current_input == "Error":
            self.current_input = ""
        if num == '.' and '.' in self.current_input:
            return
        self.current_input += num
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def input_operator(self, op):
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/', '(']:
            self.current_input += op
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
    
    def input_function(self, func):
        self.current_input += f"{func}("
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def input_constant(self, const):
        if const == 'pi':
            self.current_input += str(math.pi)
        elif const == 'e':
            self.current_input += str(math.e)
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def calculate_expression(self):
        if not self.current_input:
            return
        
        self.calculation_indicator.config(text="Calcul en cours...")
        self.root.update()
        
        try:
            expr = self.current_input
            expr = expr.replace('^', '**')
            expr = expr.replace('mod', '%')
            expr = expr.replace('π', str(math.pi))
            expr = expr.replace('e', str(math.e))
            
            if self.angle_mode == 'deg':
                expr = self.convert_trig_functions(expr, math.radians)
            
            allowed_funcs = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'log': math.log, 'log10': math.log10, 'log2': lambda x: math.log2(x),
                'exp': math.exp, 'exp2': lambda x: 2**x,
                'sqrt': math.sqrt, 'abs': abs, 'floor': math.floor, 'ceil': math.ceil,
                'gcd': math.gcd, 'lcm': lambda a,b: abs(a*b) // math.gcd(a,b) if a and b else 0
            }
            
            result = eval(expr, {"__builtins__": None}, allowed_funcs)
            
            self.history.append((self.current_input, str(result)))
            self.update_history_display()
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{self.history[-1][0]} = {result}")
            
        except Exception as e:
            self.display_error(str(e))
        finally:
            self.calculation_indicator.config(text="")
    
    def convert_trig_functions(self, expr, conversion_func):
        import re
        trig_functions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']
        for func in trig_functions:
            pattern = f"{func}\\(([^)]+)\\)"
            matches = re.findall(pattern, expr)
            for match in matches:
                try:
                    val = float(match)
                    converted_val = conversion_func(val)
                    expr = expr.replace(f"{func}({match})", f"{func}({converted_val})")
                except:
                    pass
        return expr
    
    def update_history_display(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for i, (expr, result) in enumerate(self.history):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.history_tree.insert('', 'end', values=(expr, result), tags=(tag,))
    
    def use_history_item(self, event):
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            expression = item['values'][0]
            self.current_input = expression
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
    
    def clear_history(self):
        self.history = []
        self.update_history_display()
    
    def export_history(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(self.history, f)
                
                messagebox.showinfo("Export réussi", f"Historique exporté vers {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Impossible d'exporter l'historique: {str(e)}")
    
    def import_history(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r') as f:
                    self.history = json.load(f)
                
                self.update_history_display()
                messagebox.showinfo("Import réussi", f"Historique importé depuis {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur d'import", f"Impossible d'importer l'historique: {str(e)}")
    
    def memory_clear(self):
        self.memory = 0
        self.memory_indicator.config(text=f"M: {self.memory}")
    
    def memory_recall(self):
        self.current_input = str(self.memory)
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def memory_add(self):
        try:
            value = float(self.current_input) if self.current_input else 0
            self.memory += value
            self.memory_indicator.config(text=f"M: {self.memory}")
        except:
            self.display_error("Invalid input for memory operation")
    
    def memory_subtract(self):
        try:
            value = float(self.current_input) if self.current_input else 0
            self.memory -= value
            self.memory_indicator.config(text=f"M: {self.memory}")
        except:
            self.display_error("Invalid input for memory operation")
    
    def toggle_angle_mode(self):
        self.angle_mode = 'rad' if self.angle_mode == 'deg' else 'deg'
        self.angle_indicator.config(text=f"Mode: {self.angle_mode.upper()}")
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
        self.expression_var.set("")
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else "0")
            self.expression_var.set(self.current_input)
    
    def display_error(self, message):
        self.current_input = ""
        self.result_var.set("Error")
        self.expression_var.set(f"Error: {message}")
        self.status_var.set(f"Erreur: {message}")
    
    def square_root(self):
        try:
            result = math.sqrt(float(self.current_input))
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid input for square root")
    
    def square(self):
        try:
            result = float(self.current_input) ** 2
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid input for square")
    
    def reciprocal(self):
        try:
            result = 1 / float(self.current_input)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Division by zero")
    
    def trig_function(self, func):
        try:
            angle = float(self.current_input)
            if self.angle_mode == 'deg':
                angle = math.radians(angle)
            
            if func == 'sin':
                result = math.sin(angle)
            elif func == 'cos':
                result = math.cos(angle)
            elif func == 'tan':
                result = math.tan(angle)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid trigonometric input")
    
    def factorial(self):
        try:
            n = int(float(self.current_input))
            if n < 0:
                raise ValueError("Factorial not defined for negative numbers")
            result = math.factorial(n)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid input for factorial")
    
    def negate(self):
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
    
    def convert_deg_to_rad(self):
        try:
            deg = float(self.current_input)
            rad = math.radians(deg)
            self.current_input = str(rad)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid conversion")
    
    def convert_rad_to_deg(self):
        try:
            rad = float(self.current_input)
            deg = math.degrees(rad)
            self.current_input = str(deg)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid conversion")
    
    def input_random(self):
        self.current_input = str(random.random())
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def permutation(self):
        try:
            n, r = map(int, self.current_input.split(','))
            result = math.perm(n, r)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Use format: n,r")
    
    def combination(self):
        try:
            n, r = map(int, self.current_input.split(','))
            result = math.comb(n, r)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Use format: n,r")
    
    def check_prime(self):
        try:
            n = int(float(self.current_input))
            if n < 2:
                is_prime = False
            else:
                is_prime = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
            result = "Prime" if is_prime else "Not Prime"
            self.current_input = result
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid input for prime check")
    
    def factorize(self):
        try:
            n = int(float(self.current_input))
            factors = []
            d = 2
            while d * d <= n:
                while (n % d) == 0:
                    factors.append(d)
                    n //= d
                d += 1
            if n > 1:
                factors.append(n)
            self.current_input = ' × '.join(map(str, factors))
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid input for factorization")
    
    def convert_base(self, base):
        try:
            n = int(float(self.current_input))
            if base == 16:
                result = hex(n)
            elif base == 2:
                result = bin(n)
            elif base == 8:
                result = oct(n)
            self.current_input = result
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
        except:
            self.display_error("Invalid conversion")
    
    def copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_var.get())
        self.status_var.set("Résultat copié dans le presse-papiers")
    
    def paste_input(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.current_input = clipboard_text
            self.result_var.set(self.current_input)
            self.expression_var.set(self.current_input)
            self.status_var.set("Texte collé depuis le presse-papiers")
        except:
            self.status_var.set("Impossible de coller depuis le presse-papiers")
    
    def save_calculation(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                data = {
                    "current_input": self.current_input,
                    "result": self.result_var.get(),
                    "memory": self.memory,
                    "angle_mode": self.angle_mode,
                    "history": self.history
                }
                
                with open(file_path, 'w') as f:
                    json.dump(data, f)
                
                messagebox.showinfo("Sauvegarde réussie", f"Calcul sauvegardé vers {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur de sauvegarde", f"Impossible de sauvegarder: {str(e)}")
    
    def load_calculation(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                self.current_input = data.get("current_input", "")
                self.result_var.set(data.get("result", "0"))
                self.memory = data.get("memory", 0)
                self.angle_mode = data.get("angle_mode", "deg")
                self.history = data.get("history", [])
                
                self.expression_var.set(self.current_input)
                self.memory_indicator.config(text=f"M: {self.memory}")
                self.angle_indicator.config(text=f"Mode: {self.angle_mode.upper()}")
                self.update_history_display()
                
                messagebox.showinfo("Chargement réussi", f"Calcul chargé depuis {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur de chargement", f"Impossible de charger: {str(e)}")
    
    def new_calculation(self):
        self.clear()
        self.memory_clear()
        self.history = []
        self.update_history_display()
        self.status_var.set("Nouveau calcul")
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        self.status_var.set("Plein écran" if self.fullscreen else "Fenêtre normale")
    
    def exit_fullscreen(self):
        if self.fullscreen:
            self.toggle_fullscreen()
    
    def change_theme(self):
        try:
            color = colorchooser.askcolor(initialcolor=self.theme_colors['display_fg'])
            if color[1]:
                self.theme_colors['display_fg'] = color[1]
                self.update_styles()
                self.status_var.set("Thème mis à jour")
        except:
            self.status_var.set("Impossible de changer le thème")
    
    def open_preferences(self):
        prefs_window = tk.Toplevel(self.root)
        prefs_window.title("Préférences")
        prefs_window.geometry("400x300")
        prefs_window.configure(bg=self.theme_colors['bg'])
        
        options_frame = ttk.Frame(prefs_window, style='Futuristic.TFrame')
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(options_frame, text="Précision décimale:", 
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).grid(row=0, column=0, sticky='w', pady=5)
        
        precision_var = tk.IntVar(value=10)
        precision_spinbox = ttk.Spinbox(options_frame, from_=1, to=20, textvariable=precision_var)
        precision_spinbox.grid(row=0, column=1, sticky='w', pady=5)
        
        ttk.Button(options_frame, text="Sauvegarder", style='OpButton.TButton',
                  command=lambda: self.save_preferences(precision_var.get(), "Standard", prefs_window)).grid(row=2, column=0, columnspan=2, pady=10)
    
    def save_preferences(self, precision, format_type, window):
        try:
            settings = {
                "precision": precision,
                "format": format_type,
                "angle_mode": self.angle_mode,
                "theme_colors": self.theme_colors
            }
            
            with open("calculator_settings.json", "w") as f:
                json.dump(settings, f)
            
            self.status_var.set("Préférences sauvegardées")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les préférences: {str(e)}")
    
    def load_settings(self):
        try:
            with open("calculator_settings.json", "r") as f:
                settings = json.load(f)
            
            self.angle_mode = settings.get("angle_mode", "deg")
            self.theme_colors = settings.get("theme_colors", self.theme_colors)
            
            self.angle_indicator.config(text=f"Mode: {self.angle_mode.upper()}")
            self.update_styles()
            
            self.status_var.set("Paramètres chargés")
        except:
            self.status_var.set("Utilisation des paramètres par défaut")
    
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Aide")
        help_window.geometry("600x400")
        help_window.configure(bg=self.theme_colors['bg'])
        
        help_text = scrolledtext.ScrolledText(help_window, bg=self.theme_colors['display_bg'], 
                                            fg=self.theme_colors['display_fg'],
                                            font=('Courier', 10))
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
AIDE DE LA CALCULATRICE QUANTUM (Light)

ONGLETS:
- Basic: Opérations arithmétiques de base
- Scientific: Fonctions scientifiques avancées
- History: Historique des calculs

RACCOURCIS CLAVIER:
- Ctrl+C: Copier le résultat
- Ctrl+V: Coller depuis le presse-papiers
- Ctrl+S: Sauvegarder le calcul
- Ctrl+O: Ouvrir un calcul
- F11: Plein écran
- Échap: Quitter le plein écran
- Entrée: Calculer
- Retour arrière: Supprimer le dernier caractère

MÉMOIRE:
- MC: Effacer la mémoire
- MR: Rappeler la mémoire
- M+: Ajouter à la mémoire
- M-: Soustraire de la mémoire

MODES:
- Mode angle: Degrés/Radians (basculable via le menu Affichage)

EXPORT/IMPORT:
- Vous pouvez exporter et importer l'historique des calculs
- Les calculs peuvent être sauvegardés au format JSON
        """
        
        help_text.insert(1.0, help_content)
        help_text.config(state='disabled')
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("À propos")
        about_window.geometry("400x300")
        about_window.configure(bg=self.theme_colors['bg'])
        
        about_frame = ttk.Frame(about_window, style='Futuristic.TFrame')
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(about_frame, text="Quantum Calculator ∞ Pro (Light)", 
                 font=('Arial', 16, 'bold'),
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).pack(pady=10)
        
        ttk.Label(about_frame, text="Version 2.0 Lite", 
                 font=('Arial', 12),
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).pack(pady=5)
        
        ttk.Label(about_frame, text="Une calculatrice scientifique avancée", 
                 font=('Arial', 10),
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).pack(pady=5)
        
        ttk.Label(about_frame, text="sans dépendances externes.", 
                 font=('Arial', 10),
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).pack(pady=5)
        
        ttk.Label(about_frame, text="© 2023 Quantum Calculator Team", 
                 font=('Arial', 10),
                 foreground=self.theme_colors['display_fg'], 
                 background=self.theme_colors['bg']).pack(pady=20)
        
        ttk.Button(about_frame, text="OK", style='OpButton.TButton',
                  command=about_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumCalculator(root)
    root.mainloop()