from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, mail,immagine,tipo):
        self.id = id
        self.nome = nome
        self.email = mail
        self.immagine = immagine
        self.tipo = tipo
