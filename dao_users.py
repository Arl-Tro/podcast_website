import sqlite3
from database import get_connection

def create_user(nome,mail,formato_immagine,password,tipo):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("INSERT INTO Utenti(NOME,MAIL,FORMATO_IMMAGINE,PASSWORD,TIPO) VALUES (?,?,?,?,?)",(nome,mail,formato_immagine,password,tipo)) 
        con.commit()
        id=cursor.lastrowid
        cursor.close()

    return id

def mail_taken(mail):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Utenti WHERE MAIL=?;",(mail,)) 
        utente=cursor.fetchone()
        cursor.close()
    
    return utente is not None



def get_user_by_id(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Utenti WHERE ID=?;",(id,)) 
        utente=cursor.fetchone()
        cursor.close()

    return utente


def get_user_by_email(mail):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Utenti WHERE MAIL=?;",(mail,)) 
        utente=cursor.fetchone()
        cursor.close()
    
    return utente