from tkinter import  *
from tkinter import ttk
from tkinter import messagebox
import PersonaDatos as crud

#ventana
v = Tk()
ancho = 450
alto = 400
x_v = v.winfo_screenwidth() // 2 - ancho //2
x_y = v.winfo_screenheight() // 2 - ancho //2
pos = str(ancho) + "x" + str(alto) + "+" + str(x_v) + "+" + str(x_y)
v.geometry(pos)
v.state("zoomed")
v.configure(bg="#fff")

########## VARIABLES #####################
txt_id = StringVar()
txt_dni = StringVar()
txt_nombre = StringVar()
txt_apellido = StringVar()
txt_direccion = StringVar()
txt_correo = StringVar()
txt_edad = StringVar()

##############FUNCIONES#####################
def creditos():
    messagebox.showinfo("Créditos",
                        """
                        Creado por: Martín Goñi
                        -----------------------
                        """
                        )
    
def salir():
    res = messagebox.askquestion("Salir", "Desea salir de la aplicación?")
    if res == "yes":
        v.destroy()

def llenarTabla():
    tabla.delete(*tabla.get_children())
    res = crud.findAll()
    personas = res.get("personas")
    for fila in personas:
        row = list(fila)
        row.pop(0)
        row = tuple(row)
        tabla.insert("", END, text=id, values=row)

def limpiarCampos():
    txt_dni.set("")
    txt_nombre.set("")
    txt_apellido.set("")
    txt_direccion.set("")
    txt_correo.set("")
    txt_edad.set("")
    e_dni.focus()

def guardar():
    if txt_edad.get().isnumeric():
        per = {"dni":txt_dni.get(),
               "edad":int(txt_edad.get()),
               "nombre":txt_nombre.get(),
               "apellido":txt_apellido.get(),
               "direccion":txt_direccion.get(),
               "correo":txt_correo.get()
               }
        res = crud.save(per)
        if res.get("respuesta"):
            llenarTabla()
            messagebox.showinfo("OK", res.get("mensaje"))
            limpiarCampos()
        else:
            messagebox.showerror("Ups!", res.get("mensaje"))
    else:
        txt_edad.set("")
        e_edad.focus()
        messagebox.showerror("Upps!!", "La edad debe ser númerica")
        
def consultar():
    if txt_dni.get()!= "":
        res = crud.find(txt_dni.get())
        if res.get("respuesta"):
            persona = res.get("persona")
            txt_nombre.set(persona.get("nombre"))
            txt_apellido.set(persona.get("apellido"))
            txt_direccion.set(persona.get("direccion"))
            txt_correo.set(persona.get("correo"))
            txt_edad.set(persona.get("edad"))
        else:
            e_dni.focus()
            limpiarCampos()
            messagebox.showerror("No existe la persona")
    else:
        e_dni.focus()
        limpiarCampos()
        messagebox.showerror("Debe ingresar el DNI de la persona")

def actualizar():
    if txt_edad.get().isnumeric():
        per = {
                "dni":txt_dni.get(),
                "edad":int(txt_edad.get()),
                "nombre":txt_nombre.get(),
                "apellido":txt_apellido.get(),
                "direccion":txt_direccion.get(),
                "correo":txt_correo.get()
                }
        res = crud.update(per)
        if res.get("respuesta"):
            llenarTabla()
            messagebox.showinfo("ok", res.get("mensaje"))
            limpiarCampos()
        else:
            messagebox.showerror("Ups", res.get("mensaje"))

def eliminar():
    if txt_dni.get() != "":
        res = crud.find(txt_dni.get())
        if res.get("respuesta"):
            per = res.get("persona")
            respuesta = messagebox.askquestion("Confirmar", "Realmente desea eliminar a {nombre} {apellido}?".format(nombre=per.get("nombre"), apellido=per.get("apellido")))
            if respuesta == "yes":
                res = crud.delete(per.get("id"))
                if res.get("respuesta"):
                    llenarTabla()
                    limpiarCampos()
                    messagebox.showinfo("Ok", res.get("mensaje"))
                else:
                    messagebox.showwarning("Ups!", "No se logro eliminar a la persona" + res.get("mensaje"))
            else:
                messagebox.showwarning("No existe la persona")
                limpiarCampos()
        else:
            e_dni.focus()
            messagebox.showerror("Debe indicar el dni")

#############FIN FUNCIONES#################

#############GUI##########################

fuente = ("Verdana", 12)
Label(v, text="DNI:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=0, column=0)
Label(v, text="Nombre:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=1, column=0)
Label(v, text="Apellido:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=2, column=0)
Label(v, text="Dirección:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=3, column=0)
Label(v, text="Correo:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=4, column=0)
Label(v, text="Edad:", anchor="w", justify="left", width=10, bg="#fff", font=fuente, padx=10, pady=5).grid(row=5, column=0)

########INPUTS#########

e_dni = ttk.Entry(v, font=fuente, textvariable=txt_dni)
e_nombre = ttk.Entry(v, font=fuente, textvariable=txt_nombre)
e_apellido = ttk.Entry(v, font=fuente, textvariable=txt_apellido)
e_direccion = ttk.Entry(v, font=fuente, textvariable=txt_direccion)
e_correo = ttk.Entry(v, font=fuente, textvariable=txt_correo)
e_edad = ttk.Entry(v, font=fuente, textvariable=txt_edad)

e_dni.grid(row=0, column=1)
e_nombre.grid(row=1, column=1)
e_apellido.grid(row=2, column=1)
e_direccion.grid(row=3, column=1)
e_correo.grid(row=4, column=1)
e_edad.grid(row=5, column=1)

iconNew = PhotoImage(file="new.png")
iconFind = PhotoImage(file="find.png")
iconUpdate = PhotoImage(file="update.png")
iconDelete = PhotoImage(file="delete.png")

#BOTONES

ttk.Button(v, text="Guardar", command=guardar, image=iconNew, compound=LEFT).place(x=10, y=220)
ttk.Button(v, text="Consultar", command=consultar, image=iconFind, compound=LEFT).place(x=120, y=220)
ttk.Button(v, text="Actualizar", command=actualizar, image=iconUpdate, compound=LEFT).place(x=230, y=220)
ttk.Button(v, text="Eliminar", command=eliminar, image=iconDelete, compound=LEFT).place(x=340, y=220)

Label(v, text="Lista de personas", font=("Arial", 16), bg="#fff").place(x=700, y=5)
tabla = ttk.Treeview(v)
tabla.place(x=450, y=40)
tabla["columns"] = ("DNI", "EDAD", "NOMBRE", "APELLIDO", "DIRECCION", "CORREO")
tabla.column('#0', width=0, stretch=NO)
tabla.column("DNI", width=100, anchor=CENTER)
tabla.column("EDAD", width=100, anchor=CENTER)
tabla.column("NOMBRE", width=150, anchor=CENTER)
tabla.column("APELLIDO", width=150, anchor=CENTER)
tabla.column("DIRECCION", width=160, anchor=CENTER)
tabla.column("CORREO", width=160, anchor=CENTER)

tabla.heading("#0", text="")
tabla.heading("DNI", text="DNI")
tabla.heading("EDAD", text="Edad")
tabla.heading("NOMBRE", text="Nombre")
tabla.heading("APELLIDO", text="Apellido")
tabla.heading("DIRECCION", text="Dirección")
tabla.heading("CORREO", text="Correo")

######### MENU ############
menuTop = Menu(v) ##barra menu
m_archivo = Menu(menuTop, tearoff=0)
m_archivo.add_command(label="Créditos", command=creditos)
m_archivo.add_command(label="Salir", command=salir)
menuTop.add_cascade(label="Archivo", menu=m_archivo)

m_limpiar = Menu(menuTop, tearoff=0)
m_limpiar.add_command(label="Limpiar campos", command=limpiarCampos)
menuTop.add_cascade(label="Limpiar", menu=m_limpiar)

m_crud = Menu(menuTop, tearoff=0)
m_crud.add_command(label="Guardar", command=guardar,image=iconNew, compound=LEFT)
m_crud.add_command(label="Consultar", command=consultar, image=iconFind, compound=LEFT)
m_crud.add_command(label="Actualizar", command=actualizar, image=iconUpdate, compound=LEFT)
m_crud.add_command(label="Eliminar", command=eliminar, image=iconDelete, compound=LEFT)
menuTop.add_cascade(label="CRUD", menu=m_crud)

v.config(menu=menuTop)

e_dni.focus()

llenarTabla()
v.mainloop()