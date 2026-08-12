import tkinter as tk 
import sqlite3

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tiendas 3B")
        self.geometry("500x500")
        self.resizable(False, False)

        # Aquí agregamos el menú dentro de la ventana
        menu = Menu(self)
        menu.pack(fill="both", expand=True)

class DataBases(tk.Frame):
    ...

class Menu(tk.Frame):
    def __init__(self, master): #master = WIDGET DONDE SE DIBUJARA UN NUEVO WIDGET
        super().__init__(master)

        frame_s = tk.Frame(self)
        frame_s.grid(row=0, column=0, columnspan=2)

        label = tk.Label(frame_s, text="Menú Principal", font=("Verdana", 14))
        label.grid(row=0, column=2, columnspan=4)

        botonC = tk.Button(frame_s, text="Agregar", font=("Verdana", 14))
        botonC.grid(row=1, column=0, padx=10, pady=10)

        botonR = tk.Button(frame_s, text="Consultar", font=("Verdana", 14))
        botonR.grid(row=2, column=0, padx=10, pady=10)

        botonU = tk.Button(frame_s, text="Actualizar", font=("Verdana", 14))
        botonU.grid(row=3, column=0, padx=10, pady=10)

        botonD = tk.Button(frame_s, text="Eliminar",font=("Verdana", 14))
        botonD.grid(row=4, column=0, padx=10, pady=10)

    
class UsuariosFrame(tk.Frame):
    ...

app = Ventana()
app.mainloop()
