import conexion as con

def save(persona):
    persona = dict(persona)
    try:
        db = con.conectar()
        cursor = db.cursor()
        columnas = tuple(persona.keys())
        valores = tuple(persona.values())
        sql = """
        INSERT INTO personas{campos} VALUES(?,?,?,?,?,?)
        """.format(campos=columnas)
        cursor.execute(sql, (valores))
        creada = cursor.rowcount > 0
        db.commit()
        if creada:
            cursor.close()
            db.close()
            return {"respuesta":creada, "mensaje":"Persona registrada"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":creada, "mensaje":"No se logró registrar a la persona"}
    except Exception as ex:
        if "UNIQUE" in str(ex) and "correo" in str(ex):
            mensaje = "Ya existe una persoan con ese correo"
        elif "UNIQUE" in str(ex) and "dni" in str(ex):
            mensaje = "Ya existe una persona con ese dni"
        else:
            mensaje = str(ex)
            cursor.close()
            db.close()
        return {"respuesta":False, "mensaje": mensaje}
        

def findAll():
    try:
        db = con.conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas")
        personas = cursor.fetchall()
        if personas:
            cursor.close()
            db.close()
            return {"respuesta":True, "personas":personas, "mensaje":"Listado ok"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":False, "personas":personas ,"mensaje":"No hay personas registradas aún"}
    except Exception as ex:
        cursor.close()
        db.close()
        return {"respuesta":False, "mensaje":str(ex)}
    
def find(dniPersona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas WHERE dni='{dniPersona}'".format(dniPersona=dniPersona))
        res = cursor.fetchall()
        if res:
            info = res[0]
            persona = {"id":info[0], "dni":info[1], "edad":info[2] ,"nombre":info[3], "apellido":info[4], "direccion":info[5], "correo":info[6]}
            cursor.close()
            db.close()
            return {"respuesta":True, "persona":persona, "mensaje":"Persona encontrada"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":False, "mensaje":"No existe la persona"}
    except Exception as ex:
        cursor.close()
        db.close()
        return {"respuesta":False, "mensaje":str(ex)}
    
def update(persona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        persona = dict(persona)
        dniPersona = persona.get('dni')
        persona.pop('dni')
        valores = tuple(persona.values())
        sql = """
        UPDATE personas
        SET edad=?, nombre=?, apellido=?, direccion=?, correo=?
        WHERE dni='{dni}'
        """.format(dni=dniPersona)
        cursor.execute(sql, (valores))
        modificada = cursor.rowcount > 0
        db.commit()
        cursor.close()
        db.close()
        if modificada:
            return {"respuesta":modificada, "mensaje":"Persona actualizada"}
        else:
            return {"respuesta":modificada, "mensaje":"No existe la persona con ese dni"}
    except Exception as ex:
        if "UNIQUE" in str(ex) and "correo" in str(ex):
            mensaje = "Ya existe una persona con ese correo"
        else:
            mensaje = str(ex)
            cursor.close()
            db.close()
            return {"respuesta":False, "mensaje":mensaje}
    
def delete(idPersona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        sql = """
        DELETE FROM personas WHERE id='{id}'
        """.format(id=idPersona)
        cursor.execute(sql)
        eliminada = cursor.rowcount > 0
        db.commit()
        cursor.close()
        db.close()
        if eliminada:
            return {"respuesta":eliminada, "mensaje":"Persona eliminada"}
        else:
            return {"respuesta":eliminada, "mensaje":"No existe la persona con ese ID"}
    except Exception as ex:
            cursor.close()
            db.close()
            return {"respuesta":False, "mensaje":str(ex)}