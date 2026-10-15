from database import get_connection
import datetime

def get_episodes_by_serie(id_serie):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Episodi WHERE ID_SERIE=?;",(id_serie,)) 
        episodi=cursor.fetchall()
        cursor.close()
        
    return episodi 

def get_episode_by_id(id_episodio):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Episodi WHERE ID=?;",(id_episodio,)) 
        episodio=cursor.fetchone()
        cursor.close()
        
    return episodio

def delate_episode(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("DELETE FROM Episodi WHERE ID=?;",(id,)) 
        con.commit()
        cursor.close()

def get_comment_by_episode(id_episode):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Commenti WHERE ID_EPISODIO=?;",(id_episode,)) 
        commenti=cursor.fetchall()
        cursor.close()
        
    return commenti

def get_comment_by_id(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Commenti WHERE ID=?;",(id,)) 
        commenti=cursor.fetchone()
        cursor.close()
        
    return commenti



def crea_episodio(id_serie, titolo, formato, descrizione, data):
    data = datetime.date.today()
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Episodi(ID_SERIE, TITOLO, FORMATO_AUDIO, DESCRIZIONE, DATA_EPISODIO) VALUES (?,?,?,?,?);",
            (id_serie, titolo, formato, descrizione, data)
        )
        con.commit()
        id = cursor.lastrowid
        cursor.close()
    
    return id

def modifica_episodio(id, titolo, formato, descrizione_episodio, data):
    data = datetime.date.today()
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE Episodi SET TITOLO = ?, FORMATO_AUDIO = ?, DESCRIZIONE = ?, DATA_EPISODIO = ? WHERE ID = ?;",
            (titolo, formato, descrizione_episodio, data, id)
        )
        con.commit()
        id = cursor.lastrowid
        cursor.close()
    
    return id


def aggiungi_commento(id_autore, id_episodio, commento):
    data = datetime.date.today()
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Commenti(ID_AUTORE, ID_EPISODIO, COMMENTO, DATA_COMMENTO) VALUES (?,?,?,?);",
            (id_autore, id_episodio, commento, data.isoformat())
        )
        con.commit()
        cursor.close()


def delate_comment(id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("DELETE FROM Commenti WHERE ID=?;",(id,)) 
        con.commit()
        cursor.close()

def change_comment(commento, id):
    with get_connection() as con:
        cursor=con.cursor()
        cursor.execute("UPDATE Commenti SET COMMENTO=? WHERE ID=?;",(commento,id,)) 
        con.commit()
        cursor.close()
         
    return commento
