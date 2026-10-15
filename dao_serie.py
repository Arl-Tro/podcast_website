from database import get_connection

def get_all_series():
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Serie;") 
        serie=cursor.fetchall()
        cursor.close()
        
    return serie

def get_serie_by_categoria(categoria):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Serie WHERE CATEGORIA=?;", (categoria,)) 
        serie=cursor.fetchall()
        cursor.close()
        
    return serie


def get_seguiti(id_utente):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT S.* FROM Serie S, Serie_seguite SS WHERE S.ID = SS.ID_SERIE AND SS.ID_UTENTE = ?;", (id_utente,))
        seguiti = cursor.fetchall()
        cursor.close()
    
    return seguiti

def get_categorie():
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT DISTINCT CATEGORIA FROM Serie;")
        category = cursor.fetchall()
        cursor.close()
    
    return category

def get_serie_by_id(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Serie WHERE ID=?;",(id,)) 
        serie=cursor.fetchone()
        cursor.close()
        
    return serie 
 
def utente_segue(id_utente, id_serie):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Serie_seguite WHERE ID_UTENTE=? AND ID_SERIE=?;",(id_utente, id_serie)) 
        segue=cursor.fetchone() is not None
        cursor.close()
        
    return segue 

def segui(id_utente, id_serie):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("INSERT INTO Serie_seguite(ID_UTENTE, ID_SERIE) VALUES (?,?);",(id_utente, id_serie)) 
        con.commit()
        cursor.close()
        

def unsegui(id_utente, id_serie):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("DELETE FROM Serie_seguite WHERE ID_UTENTE=? AND ID_SERIE=?;",(id_utente, id_serie)) 
        con.commit()
        cursor.close()

def create_serie(id_autore,titolo,formato_immagine,descrizione,categoria):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("INSERT INTO Serie(ID_AUTORE,TITOLO,FORMATO_IMMAGINE,DESCRIZIONE,CATEGORIA) VALUES (?,?,?,?,?)",(id_autore,titolo,formato_immagine,descrizione,categoria)) 
        con.commit()
        id=cursor.lastrowid
        cursor.close()
        
    return id

def delate_serie(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("DELETE FROM Serie WHERE ID=?;",(id,)) 
        con.commit()
        cursor.close()
        

def edit_info_serie(id,titolo,descrizione,categoria):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("UPDATE Serie SET TITOLO=?,DESCRIZIONE=?,CATEGORIA=? WHERE ID=?;",(titolo,descrizione,categoria,id)) 
        con.commit()
        cursor.close()
        

def edit_image_serie(id,formato_immagine):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("UPDATE Serie SET FORMATO_IMMAGINE=? WHERE ID=?;",(formato_immagine,id)) 
        con.commit()
        cursor.close()
        

