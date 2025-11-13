import customtkinter as ctk

class PaginaBase(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configurar_grid()
        self.crear_widgets()
        
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def crear_widgets(self):
        pass
    
    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")
    
    def limpiar(self):
        for widget in self.winfo_children():
            widget.destroy()