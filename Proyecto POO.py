import tkinter as tk 
import sqlite3
from tkinter import messagebox
class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tiendas 3B")
        self.geometry("500x500")
        self.resizable(False, False)

        self.databases = DataBases()
        
        self.menu = Menu(self,self.mostrar_guardar,self.mostrar_productos,self.mostrar_actualizar,self.mostrar_borrar)
        self.menu.grid()

        self.agregar = Agregar(self,self.databases,self.mostrar_inicio)
        self.agregar.grid_remove()

        self.consultar = Consultar(self,self.mostrar_inicio,self.databases)
        self.consultar.grid_remove()

        self.actualizar = Actualizar(self,self.mostrar_inicio,self.databases)
        self.actualizar.grid_remove()

        self.borrado = Eliminar(self,self.mostrar_inicio,self.databases)
        self.borrado.grid_remove()

    def mostrar_inicio (self):
        self.menu.grid()
        self.agregar.grid_remove()
        self.consultar.grid_remove()
        self.actualizar.grid_remove()
        self.borrado.grid_remove()

    def mostrar_guardar (self):
        self.menu.grid_remove()
        self.agregar.grid(row=0,column=0)

    def mostrar_productos (self):
        self.menu.grid_remove()
        self.agregar.grid_remove()
        self.consultar.grid(row=0,column=1,columnspan=2)
        self.databases.cargar_lista(self.consultar.listbox)

    def mostrar_actualizar (self):
        self.menu.grid_remove()
        self.agregar.grid_remove()
        self.consultar.grid_remove()
        self.actualizar.grid()
        self.databases.cargar_lista(self.actualizar.listbox)

    def mostrar_borrar (self):
        self.menu.grid_remove()
        self.agregar.grid_remove()
        self.consultar.grid_remove()
        self.actualizar.grid_remove()
        self.borrado.grid()
        self.databases.cargar_lista(self.borrado.listbox)
         
        

class Entrada():
    def __init__(self,nombre,precio,stock):
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
    
    @property
    def nombre (self):
        return self.__nombre

    @property
    def precio (self):
        return self.__precio
    
    @property
    def stock (self):
        return self.__stock
 
class DataBases():
    def __init__(self):
        self.conn = sqlite3.connect("tienda.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio TEXT NOT NULL,
                stock REAL NOT NULL
            )
        """)
        self.conn.commit()

    def agregar(self, producto):
        self.cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (producto.nombre, producto.precio, producto.stock)
        )
        self.conn.commit()
        

    def actualizar (self,producto,id_producto):
        self.cursor.execute(
            "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
            (producto.nombre,producto.precio,producto.stock,id_producto)
        )
        self.conn.commit()
        
    def borrar (self,id_producto):
            self.cursor.execute(
                "DELETE FROM productos WHERE id = ?",
                (id_producto,)
            )
            self.conn.commit()
            

    def cargar_lista(self, listbox):
        listbox.delete(0, "end")

        self.cursor.execute(
            "SELECT id, nombre, precio, stock FROM productos"
        )

        for fila in self.cursor.fetchall():
            listbox.insert(
                "end",
                f"{fila[0]}|{fila[1]}|{fila[2]}|{fila[3]}"
            )



class Menu(tk.Frame):
    def __init__(self, master,mostrar_guardar,mostrar_productos,mostrar_actualizar,mostrar_borrar): #master = WIDGET DONDE SE DIBUJARA UN NUEVO WIDGET
        super().__init__(master)

        self.mostrar_guardar = mostrar_guardar
        self.mostrar_productos = mostrar_productos
        self.mostrar_actualizar = mostrar_actualizar
        self.mostrar_borrar = mostrar_borrar

        label = tk.Label(self, text="Menú Principal", font=("Verdana", 14))
        label.grid(row=0, column=2, columnspan=4)

        botonC = tk.Button(self, text="Agregar Producto", font=("Verdana", 14),command=mostrar_guardar)
        botonC.grid(row=1, column=0, padx=10, pady=10)

        botonR = tk.Button(self, text="Consultar Productos", font=("Verdana", 14),command=mostrar_productos)
        botonR.grid(row=2, column=0, padx=10, pady=10)

        botonU = tk.Button(self, text="Actualizar Producto", font=("Verdana", 14),command=mostrar_actualizar)
        botonU.grid(row=3, column=0, padx=10, pady=10)

        botonD = tk.Button(self, text="Eliminar Producto",font=("Verdana", 14),command=mostrar_borrar)
        botonD.grid(row=4, column=0, padx=10, pady=10)

class Agregar(tk.Frame):
    def __init__ (self,master,databases,mostrar_inicio):
        super().__init__(master)

        self.databases = databases
        self.mostrar_inicio = mostrar_inicio

        label = tk.Label(self,text="Introduzca el nombre del Producto",font=("Verdana",12))
        label.grid(row=1,column=0)

        self.nombre = tk.Entry (self)
        self.nombre.grid(row=1,column=1)

        label1 = tk.Label(self,text="Introduzca el precio del Producto",font=("Verdana",12))
        label1.grid(row=2,column=0)
        
        self.precio = tk.Entry (self)
        self.precio.grid(row=2,column=1)

        label = tk.Label(self,text="Introduzca el stock del Producto",font=("Verdana",12))
        label.grid(row=3,column=0)
        
        self.stock = tk.Entry (self)
        self.stock.grid(row=3,column=1)

        boton_guardar = tk.Button(self,text="Guardar",font=("Verdana",12),command=self.guardar)
        boton_guardar.grid(row=4,column=0,columnspan=2)

        boton_inicio = tk.Button(self,text="Regresar al Inicio",font=("Verdana",12),command=mostrar_inicio)
        boton_inicio.grid(row=4,column=1,columnspan=2)

    def guardar(self):
        nombre = self.nombre.get()
        precio = self.precio.get()
        stock = self.stock.get()
        if nombre == "" or precio == "" or stock == "":
            messagebox.showwarning("ADVERTENCIA",
                                "LLENE TODOS LOS CAMPOS")
            return
        try:
            precio = float(precio)
            stock = int(stock)
        except:
            messagebox.showwarning("ADVERTENCIA",
                                "ERROR EN LOS DATOS")
            return
        else:
            messagebox.showinfo("LISTO",
                                    "PRODUCTO GUARDADO")

        producto = Entrada(nombre, precio, stock)
        self.databases.agregar(producto)
        self.nombre.delete(0, "end")
        self.precio.delete(0, "end") #borra los datos una vez regsitrados
        self.stock.delete(0, "end")
        

class Consultar(tk.Frame):
    def __init__(self,master,mostrar_inicio,databases):
        super().__init__(master)

        self.databases = databases

        self.mostrar_inicio = mostrar_inicio
        label = tk.Label(self,text="Productos en Almacen",font=("Verdana",12))
        label.grid(row=0,column=2,columnspan=4)


        self.listbox = tk.Listbox(
        self,
        width=40,
        height=8,
        exportselection=False #mantiene seleccionado un elemento aunque hagas clic en otro boton
        )
        self.listbox.grid(row=2, column=2, columnspan=4)


        boton_inicio = tk.Button(self,text="Regresar al Inicio",font=("Verdana",12),command=mostrar_inicio)
        boton_inicio.grid(row=4,column=1,columnspan=2)


class Actualizar (tk.Frame):

    def __init__(self,master,mostrar_inicio,databases):
        super().__init__(master)

        self.databases = databases
        self.mostrar_inicio = mostrar_inicio
        
        label = tk.Label(self,text="Seleccione un Producto Para Actualizarlo",font=("Verdana",12))
        label.grid(row=0,column=0,columnspan=2)
        
        self.listbox = tk.Listbox(
        self,
        width=40,
        height=8,
        exportselection=False) #mantiene seleccionado un elemento aunque hagas clic en otro boton
        
        self.listbox.grid(row=1, column=0, columnspan=2)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar)

        
        self.databases.cursor.execute( "SELECT id, nombre, precio, stock FROM productos")
        for fila in self.databases.cursor.fetchall(): 
                        self.listbox.insert("end", f"{fila[0]}|{fila[1]}|{fila[2]}|{fila[3]}")
        
        label_nombre = tk.Label(self, text="Nuevo nombre:",font=("Verdana",12))
        label_nombre.grid(row=3, column=0)
        
        self.nombre = tk.Entry(self)
        self.nombre.grid(row=3, column=1)
        
        label_precio = tk.Label(self,text="Nuevo precio:",font=("Verdana",12))
        label_precio.grid(row=4,column=0)
        
        self.precio = tk.Entry(self)
        self.precio.grid(row=4, column=1)
        
        label_stock = tk.Label(self,text="Nuevo stock:",font=("Verdana",12))
        label_stock.grid(row=5,column=0)
        
        self.stock = tk.Entry(self)
        self.stock.grid(row=5, column=1)
        
        boton_inicio = tk.Button(self,text="Regresar al Inicio",font=("Verdana",12),command=mostrar_inicio)
        boton_inicio.grid(row=6,column=1)
        
        boton_actualizar = tk. Button (self,text="Actualizar",font=("Verdana",12),command=self.actualizacion)
        boton_actualizar.grid(row=6,column=0)

        # aquí conectamos el evento
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar)

            
    def seleccionar(self, event):
            seleccion = self.listbox.curselection()
            
            if seleccion:
                posicion = seleccion[0]
                producto = self.listbox.get(posicion)

                datos = producto.split("|")

                self.id_producto = datos[0]
                nombre = datos[1]
                precio = datos[2]
                stock = datos[3]

                self.nombre.delete(0, "end")
                self.nombre.insert(0, nombre)

                self.precio.delete(0, "end")
                self.precio.insert(0, precio)

                self.stock.delete(0, "end")
                self.stock.insert(0, stock)
                self.listbox.bind("<<ListboxSelect>>", self.seleccionar)
    def actualizacion (self):
                print("jojoa")
                nuevo_nombre = self.nombre.get()
                nuevo_precio = self.precio.get()
                nuevo_stock = self.stock.get()
        
                producto = Entrada(nuevo_nombre, nuevo_precio,nuevo_stock)
                self.databases.actualizar(producto,self.id_producto)
                self.databases.cargar_lista(self.listbox)
                self.nombre.delete(0, "end")
                self.precio.delete(0, "end") #borra los datos una vez regsitrados
                self.stock.delete(0, "end")
                messagebox.showinfo("LISTO",
                                    "PRODUCTO ACTUALIZADO")

class Eliminar (tk.Frame):
        def __init__(self,master,mostrar_inicio,databases):
             super().__init__(master)
     
             self.databases = databases
             self.mostrar_inicio = mostrar_inicio
             self.listbox = tk.Listbox(self)
     
             label = tk.Label(self,text="Seleccione un Producto Para Eliminarlo",font=("Verdana",12))
             label.grid(row=0,column=0,columnspan=2)
             
             self.listbox = tk.Listbox(
             self,
             width=40,
             height=8,
             exportselection=False) #mantiene seleccionado un elemento aunque hagas clic en otro boton
             
             self.listbox.grid(row=1, column=0, columnspan=2)
             self.listbox.bind("<<ListboxSelect>>", self.seleccionar)
             
             self.databases.cursor.execute( "SELECT id, nombre, precio, stock FROM productos")
             for fila in self.databases.cursor.fetchall(): 
                             self.listbox.insert("end", f"{fila[0]}|{fila[1]}|{fila[2]}|{fila[3]}")
             
             boton_inicio = tk.Button(self,text="Regresar al Inicio",font=("Verdana",12),command=mostrar_inicio)
             boton_inicio.grid(row=6,column=1)
             
             boton_eliminar = tk. Button (self,text="Eliminar",font=("Verdana",12),command=self.eliminar)
             boton_eliminar.grid(row=6,column=0)
     
             # aquí conectamos el evento
             self.listbox.bind("<<ListboxSelect>>", self.seleccionar)
     
                 
        def seleccionar(self, event):
                 seleccion = self.listbox.curselection()
                 
                 if seleccion:
                     posicion = seleccion[0]
                     producto = self.listbox.get(posicion)
     
                     datos = producto.split("|")
     
                     self.id_producto = datos[0]

                     self.listbox.bind("<<ListboxSelect>>", self.seleccionar)
                     
        def eliminar (self):
            self.databases.borrar(self.id_producto)     
            self.databases.cargar_lista(self.listbox)
            messagebox.showinfo("LISTO",
                                "PRODUCTO ELIMINADO")
app = Ventana()
app.mainloop()
