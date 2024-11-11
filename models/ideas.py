from config.db import connectToMySQL

class Idea:
    def __init__(self, data):
        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.idea_text = data["idea_text"]
    @classmethod
    def user_idea(cls, id_usuario):
        query = f"SELECT * FROM idea WHERE usuario_id = {id_usuario};"
        results = connectToMySQL('cn_daniel').query_db(query)
        ideas = []
        for idea in results:
            ideas.append(cls(idea))
        return ideas
    @classmethod
    def send_idea(cls, texto,id_usuraio):
        query = f"INSERT INTO idea (idea_text, usuario_id) VALUES ('{texto}', {id_usuraio});"
        results = connectToMySQL('cn_daniel').query_db(query)
        return results
    @classmethod
    def edit_idea(cls, texto,id_idea):
        query = f"UPDATE idea SET idea_text = '{texto}' WHERE id = {id_idea};"
        results = connectToMySQL('cn_daniel').query_db(query)
        return results
    @classmethod
    def del_idea(cls, id_idea):
        query = f"DELETE FROM idea WHERE id = {id_idea}"
        results = connectToMySQL('cn_daniel').query_db(query)
        return results
    @classmethod
    def get_idea(cls, id_idea):
        query = f"SELECT * FROM idea WHERE id = {id_idea};"
        results = connectToMySQL('cn_daniel').query_db(query)
        idea = cls(results[0])
        return idea

