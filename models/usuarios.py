from config.db import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
    
    @classmethod
    def ver_user(cls, email):
        query = f"SELECT * FROM usuario WHERE email = '{email}';"
        results = connectToMySQL('cn_daniel').query_db(query)
        usuarios = []
        for user in results:
            usuarios.append(cls(user))
        return usuarios
    @classmethod
    def insert_user(cls, first_name, last_name, email, password):
        query = f"INSERT INTO usuario (first_name, last_name, email, password) VALUES ('{first_name}', '{last_name}', '{email}', '{password}');"
        results = connectToMySQL('cn_daniel').query_db(query)
        return results
    @classmethod
    def select_user(cls, id_usuario):
        query = f"SELECT * FROM usuario WHERE id = {id_usuario};"
        results = connectToMySQL('cn_daniel').query_db(query)
        return results