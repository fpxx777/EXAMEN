from config.db import connectToMySQL

class Idea_Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.idea_text = data["idea_text"]
        self.first_name = data["first_name"]
        self.last_name = data['last_name']
    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM idea JOIN usuario ON usuario_id = usuario.id;"
        results = connectToMySQL('cn_daniel').query_db(query)
        ideas = []
        for idea in results:
            ideas.append(cls(idea))
        return ideas