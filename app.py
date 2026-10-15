from flask_bootstrap import Bootstrap5

from flask import Flask, abort, redirect, render_template, request, send_from_directory, url_for,flash

from flask_session import Session

from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from user_model import User

from werkzeug.security import generate_password_hash,check_password_hash

import dao_users

import dao_serie

import dao_episodi

import os

app = Flask(__name__)

Bootstrap5(app)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"] = " bc86KUDKYU36due4IKY3Gkuyf1quk36YFQKUY6u6kyqfkuy7QUYFD6UKyqf"


@app.route("/")
def route_home():
    utenti = {}
    lista_serie=dao_serie.get_all_series()
    for serie in lista_serie:
        utenti[serie["ID"]] = dao_users.get_user_by_id(serie["ID_AUTORE"])

    return render_template("main.html", lista_serie=lista_serie, utenti=utenti)

@app.route("/categoria/<string:categoria>")
def route_categoria(categoria):
    utenti = {}
    lista_serie=dao_serie.get_serie_by_categoria(categoria)
    for serie in lista_serie:
        utenti[serie["ID"]] = dao_users.get_user_by_id(serie["ID_AUTORE"])

    return render_template("categoria.html", categoria=categoria, lista_serie=lista_serie, utenti=utenti)

@app.route("/profilo/<string:id>")
def route_creatore(id):
    return render_template("mio_profilo.html", utente=dao_users.get_user_by_id(id))

@app.route("/registrati")
def route_registrati():
    return render_template("registrati.html")

@app.route("/accedi")
def route_accedi():
    return render_template("accedi.html")


@app.route("/form_crea_serie")
def route_form_crea_serie():
    return render_template("crea_serie.html")

@app.route("/mie_serie")
@login_required
def route_mie_serie():
    serie_tutte=dao_serie.get_all_series()
    
    lista_serie = []
    for serie in serie_tutte:
        if serie["ID_AUTORE"] == current_user.id:
            lista_serie.append(serie)

    return render_template("mio_podcast.html", lista_serie=lista_serie)



@app.route("/serie/<string:id>")
def route_mostra_serie(id):
    serie = dao_serie.get_serie_by_id(id)
    episodi = dao_episodi.get_episodes_by_serie(id)

    if serie is None:
        abort(404)

    if current_user.is_authenticated:
        utente_segue_serie = dao_serie.utente_segue(current_user.id, id)
    else:
        utente_segue_serie = False

    utente = dao_users.get_user_by_id(serie["ID_AUTORE"])
    
    return render_template("visualizza_serie.html", serie=serie, episodi=episodi,utente=utente, utente_segue_serie=utente_segue_serie)

@app.route("/episodio/<string:id>")
def route_mostra_episodio(id):
    episodio = dao_episodi.get_episode_by_id(id)
    commenti = dao_episodi.get_comment_by_episode(id)

    if episodio is None:
        abort(404)

    autori = {}
    for commento in commenti:
        autori[commento["ID"]] = dao_users.get_user_by_id(commento["ID_AUTORE"])

    serie = dao_serie.get_serie_by_id(episodio["ID_SERIE"])

    if serie is None:
        abort(404)
    
    return render_template("pagina_episodio.html", serie=serie, episodio=episodio,commenti=commenti,autori=autori)




@app.route("/sign_up",methods=["POST"])
def route_sign_up():
    nome = request.form.get("nome", "")
    mail = request.form.get("mail", "")
    password = request.form.get("password", "")
    tipo = request.form.get("tipo", "")
    immagine=request.files.get("immagine")

    if len(nome)<1 or len(nome)>100:
        flash("Nome utente non valido ")
        return redirect(url_for("route_registrati"))

    if len(mail)<1 or len(mail)>100:
        flash("Mail non valida")
        return redirect(url_for("route_registrati"))

    if len(password)<5 or len(password)>100:
        flash("Password non valida : minimo 6 caratteri")
        return redirect(url_for("route_registrati"))

    if immagine is None:
        flash("Nessuna immagine inserita")
        return redirect(url_for("route_registrati"))

    if tipo not in ["Creatore","Ascoltatore"]:
        flash("Nessun tipo utente corrispondente")
        return redirect(url_for("route_registrati"))

    if dao_users.mail_taken(mail):
        flash("Utente già esistente")
        return redirect(url_for("route_registrati"))
        


    password_hash = generate_password_hash(password)

    formato = os.path.splitext(immagine.filename)[1]

    id = dao_users.create_user(nome,mail, formato, password_hash,tipo)
    immagine.save(f"immagini_utente/img_{id}{formato}")
    login_user(load_user(id))
    return redirect(url_for("route_creatore", id=id))

@app.route("/utenti/<string:id>/immagine")
def route_immagine_utente(id):
    utente = dao_users.get_user_by_id(id)

    if not utente:
        abort(404)

    percorso = f"img_{id}{utente['FORMATO_IMMAGINE']}" 

    return send_from_directory("immagini_utente", percorso)

@app.route("/serie/<string:id>/immagine")
def route_immagine_serie(id):
    serie = dao_serie.get_serie_by_id(id)

    if not serie:
        abort(404)

    percorso = f"img_{id}{serie['FORMATO_IMMAGINE']}" 

    return send_from_directory("immagini_serie", percorso)

@app.route("/episodi/<string:id>/traccia")
def route_traccia_audio(id):
    episodio = dao_episodi.get_episode_by_id(id)

    if not episodio:
        abort(404)

    percorso = f"track_{id}{episodio['FORMATO_AUDIO']}" 

    return send_from_directory("traccia_episodio", percorso)


@app.route("/login", methods=["POST"])
def route_login():
    mail = request.form.get("mail")
    password = request.form.get("password")

    if mail is None or password is None:
        flash("Inserisci una mail e la password")
        return redirect(url_for("route_accedi"))

    user = dao_users.get_user_by_email(mail)

    if user is None:
        flash("L'utente non esiste")
        return redirect(url_for("route_accedi"))

    if not check_password_hash(user["PASSWORD"],password):
        flash("La password non è corretta")
        return redirect(url_for("route_accedi"))

    login_user(load_user(user["ID"]))

    return redirect(url_for("route_home"))




@app.route("/logout", methods=["POST"])
@login_required
def route_logout():
    logout_user()
    return redirect(url_for("route_home"))


@app.route("/test")
def route_test():
    testo_lungo = "ciao " * 100
    lista = [1, 2, 3, 4]

    return render_template("test.html", testo=testo_lungo, lista=lista)

@login_manager.user_loader
def load_user(user_id):
    db_user = dao_users.get_user_by_id(user_id)

    return User(
        id=db_user["ID"],
        nome=db_user["NOME"],
        mail=db_user["MAIL"],
        immagine=db_user["FORMATO_IMMAGINE"],
        tipo=db_user["TIPO"]
    )

@app.route("/episodio/<string:id>/commenta",methods=["POST"])
@login_required
def route_create_comment(id):
    commento=request.form.get("commento",'')
    
    if len(commento)==0:
        flash("Nessun commento inserito")
        return redirect(url_for('route_mostra_episodio',id=id))

    dao_episodi.aggiungi_commento(current_user.id ,id, commento)
    return redirect(url_for('route_mostra_episodio',id=id))

@app.route("/episodio/<string:id>/togli_commento", methods=["POST"])
@login_required
def route_remove_comment(id):
    id_commento = request.form.get("id_commento", '')
    print("ID", id_commento)

    commento = dao_episodi.get_comment_by_id(id_commento)

    if commento is None:
        abort(404)

    if commento["ID_AUTORE"] != current_user.id:
        abort(401)

    dao_episodi.delate_comment(id_commento)
    return redirect(url_for('route_mostra_episodio',id=id))



@app.route("/serie/<string:id>/toggle")
def route_toggle_follow(id):
    if dao_serie.utente_segue(current_user.id, id):
        dao_serie.unsegui(current_user.id, id)
    else:
        dao_serie.segui(current_user.id, id)

    return redirect(url_for("route_mostra_serie", id=id))

@app.route("/serie/<string:id>/modifica_episodio_form")
@login_required
def route_form_modifica_episodio(id):
    episodio = dao_episodi.get_episode_by_id(id)
    return render_template("modifica_episodio.html", episodio=episodio, serie=dao_serie.get_serie_by_id(episodio["ID"]))

@app.route("/episodio/<string:episodio_id>/modifica_episodio", methods=["POST"])
@login_required
def route_modifica_episodio(episodio_id):
    titolo = request.form.get("titolo", "")
    descrizione_episodio = request.form.get("descrizione_episodio", "")
    data = request.form.get("data", "")
    traccia = request.files.get("traccia")

    episodio = dao_episodi.get_episode_by_id(episodio_id)
    serie = dao_serie.get_serie_by_id(episodio["ID_SERIE"])
    serie_id = serie["ID"]
    if serie["ID_AUTORE"] != current_user.id:
        abort(401)

    if len(titolo) < 1 or len(titolo) > 100:
        flash("Titolo della serie non valido ")
        return redirect(url_for("route_form_modifica_episodio", serie_id=serie_id))

    if len(descrizione_episodio) < 1 or len(descrizione_episodio) > 1000:
        flash("Descrizione non valida ")
        return redirect(url_for("route_form_modifica_episodio", serie_id=serie_id))

    if traccia is None:
        flash("Nessuna traccia inserita")
        return redirect(url_for("route_form_modifica_episodio", serie_id=serie_id))

    
    print(traccia)
    formato = os.path.splitext(traccia.filename)[1]

    id=episodio_id
    if os.path.exists(f"traccia_episodio/track_{id}{formato}"):
        os.remove(f"traccia_episodio/track_{id}{formato}")
    dao_episodi.modifica_episodio(id, titolo, formato, descrizione_episodio, data)

    traccia.save(f"traccia_episodio/track_{id}{formato}")

    return redirect(url_for("route_mostra_episodio", id=id))

@app.route("/serie/<string:id>/crea_episodio_form")
@login_required
def route_form_crea_episodio(id):
    return render_template("crea_episodio.html", serie=dao_serie.get_serie_by_id(id))

@app.route("/serie/<string:serie_id>/crea_episodio", methods=["POST"])
@login_required
def route_crea_episodio(serie_id):
    titolo = request.form.get("titolo", "")
    descrizione_episodio = request.form.get("descrizione_episodio", "")
    data = request.form.get("data", "")
    traccia = request.files.get("traccia")

    serie = dao_serie.get_serie_by_id(serie_id)
    if serie["ID_AUTORE"] != current_user.id:
        abort(401)

    if len(titolo)<1 or len(titolo)>100:
        flash("Titolo della serie non valido ")
        return redirect(url_for("route_form_crea_episodio", serie_id=serie_id))

    if len(descrizione_episodio)<1 or len(descrizione_episodio)>1000:
        flash("Descrizione non valida ")
        return redirect(url_for("route_form_crea_episodio", serie_id=serie_id))

    if traccia is None:
        flash("Nessuna immagine inserita")
        return redirect(url_for("route_form_crea_episodio", serie_id=serie_id))

    
    formato = os.path.splitext(traccia.filename)[1]

    id = dao_episodi.crea_episodio(serie_id, titolo, formato, descrizione_episodio, data)
    traccia.save(f"traccia_episodio/track_{id}{formato}")
    return redirect(url_for("route_mostra_episodio", id=id))

@app.route("/commento/<string:id>/modifica_commento_form")
@login_required
def route_form_modifica_commento(id):
    commento = dao_episodi.get_comment_by_id(id)

    if not commento:
        abort(404)

    episodio = dao_episodi.get_episode_by_id(commento["ID_EPISODIO"])

    if commento["ID_AUTORE"] != current_user.id:
        abort(401)

    return render_template("modifica_commento.html", episodio=episodio, commento=commento)

@app.route("/commento/<string:id>/modifica_commento", methods=["POST"])
@login_required
def route_modifica_commento(id):
    contenuto = request.form.get("commento", "")
    commento = dao_episodi.get_comment_by_id(id)

    if len(commento) < 1 or len(commento) > 1000:
        flash("Commento invalido")
        return redirect("route_form_modifica_commento", id=id)

    episodio = dao_serie.get_serie_by_id(commento["ID_EPISODIO"])

    if commento["ID_AUTORE"] != current_user.id:
        abort(401)

    dao_episodi.change_comment(contenuto, id)

    return redirect(url_for("route_mostra_episodio", id=episodio["ID"]))


@app.route("/serie/<string:id>/modifica_form")
@login_required
def route_form_modifica_serie(id):
    serie = dao_serie.get_serie_by_id(id)

    return render_template("modifica_serie.html", serie=serie)

@app.route("/serie/<string:id>/modifica", methods=["POST"])
@login_required
def route_modifica_serie(id):
    titolo = request.form.get("titolo", "")
    categoria = request.form.get("categoria", "")
    descrizione_serie = request.form.get("descrizione_serie", "")
    immagine_serie = request.files.get("immagine")

    if len(titolo)<1 or len(titolo)>100:
        flash("Titolo della serie non valido ")
        return redirect(url_for("route_form_crea_serie"))

    if len(descrizione_serie)<1 or len(descrizione_serie)>1000:
        flash("Descrizione non valida ")
        return redirect(url_for("route_form_crea_serie"))

    if len(categoria)<1 or len(categoria)>100:
        flash("Categoria non valida")
        return redirect(url_for("route_form_crea_serie"))

    if immagine_serie is None:
        flash("Nessuna immagine inserita")
        return redirect(url_for("route_form_crea_serie"))

    
    formato = os.path.splitext(immagine_serie.filename)[1]

    if os.path.exists(f"immagini_serie/img_{id}{formato}"):
        os.remove(f"immagini_serie/img_{id}{formato}")

    dao_serie.edit_info_serie(id, titolo, descrizione_serie, categoria)
    dao_serie.edit_image_serie(id, formato)

    immagine_serie.save(f"immagini_serie/img_{id}{formato}")
    return redirect(url_for("route_mostra_serie",id=id))


@app.route("/crea_serie", methods=["POST"])
@login_required
def route_crea_serie():
    titolo = request.form.get("titolo", "")
    categoria = request.form.get("categoria", "")
    descrizione_serie = request.form.get("descrizione_serie", "")
    immagine_serie = request.files.get("immagine")

    if len(titolo)<1 or len(titolo)>100:
        flash("Titolo della serie non valido ")
        return redirect(url_for("route_form_crea_serie"))

    if len(descrizione_serie)<1 or len(descrizione_serie)>1000:
        flash("Descrizione non valida ")
        return redirect(url_for("route_form_crea_serie"))

    if len(categoria)<1 or len(categoria)>100:
        flash("Categoria non valida")
        return redirect(url_for("route_form_crea_serie"))

    if immagine_serie is None:
        flash("Nessuna immagine inserita")
        return redirect(url_for("route_form_crea_serie"))

    
    formato = os.path.splitext(immagine_serie.filename)[1]

    id = dao_serie.create_serie(current_user.id, titolo, formato, descrizione_serie, categoria)
    immagine_serie.save(f"immagini_serie/img_{id}{formato}")
    return redirect(url_for("route_mostra_serie",id=id))

@app.route("/serie/<string:id>/elimina")
@login_required
def route_elimina_serie(id):
    serie = dao_serie.get_serie_by_id(id)

    if not serie:
        abort(404)
    
    if serie["ID_AUTORE"] != current_user.id:
        abort(401)

    dao_serie.delate_serie(id)

    return redirect(url_for("route_home"))

@app.route("/episodio/<string:id>/elimina")
@login_required
def route_elimina_episodio(id):
    episodio = dao_episodi.get_episode_by_id(id)
    serie = dao_serie.get_serie_by_id(episodio["ID_SERIE"])

    if not serie:
        abort(404)
    
    if serie["ID_AUTORE"] != current_user.id:
        abort(401)

    dao_episodi.delate_episode(id)

    return redirect(url_for("route_mostra_serie", id=serie["ID"]))

# https://flask.palletsprojects.com/en/2.2.x/templating/#context-processors
@app.context_processor
def inietta_categorie():

    diz = {
        "categorie": dao_serie.get_categorie()
    }

    if current_user.is_authenticated:
        seguiti = dao_serie.get_seguiti(current_user.id)
        autori = {}
        
        for serie in seguiti:
            autori[serie["ID"]] = dao_users.get_user_by_id(serie["ID_AUTORE"])

        diz["seguiti"] = seguiti
        diz["serie_seguite_autore"] = autori

    return diz