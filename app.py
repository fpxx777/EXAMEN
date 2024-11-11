from flask import Flask, render_template, redirect, session, request
from flask_bcrypt import Bcrypt

from models.usuarios import Usuario
from models.ideas import Idea
from models.idea_usuario import Idea_Usuario

app = Flask(__name__)

app.secret_key = 'P4$$W0RD'

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def login_register():
    return render_template('login&register.html')

@app.route('/process', methods=['POST'])
def process():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    errors = []
    is_user = Usuario.ver_user(email)
    if len(is_user) > 0: 
        errors.append('Este gmail ya esta registrado')
        print(errors)
        return render_template('login&register.html', errors=errors)
    elif not password == confirm_password:
        errors.append('Las contraseñas no coinciden')
        return render_template('login&register.html', errors=errors)
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        Usuario.insert_user(first_name, last_name, email, hashed_password)
        errors.append('ok')
        return render_template('login&register.html', errors=errors)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email_login')
    password = request.form.get('password_login')

    login_errors = []
    is_user = Usuario.ver_user(email)
    if len(is_user) != 1:
        login_errors.append('Este gmail no esta registrado, registrate para iniciar sesion!!')
        return render_template('login&register.html', login_errors=login_errors)
    user = is_user[0]
    print(user.password)
    if not bcrypt.check_password_hash(user.password, password):
        login_errors.append("El gmail y/o la contraseñas no coinciden")
        return render_template("login&register.html", login_errors=login_errors)
    else:
        session["id"] = user.id
        session["first_name"] = user.first_name
        session["last_name"] = user.last_name
        return redirect('/ideas')

@app.route('/ideas', methods=['GET'])
def ideas():
    ideas = Idea_Usuario.get_all()
    return render_template("ideas.html", session=session, ideas=ideas)

@app.route('/ideas/send', methods=['POST'])
def send():
    idea = request.form.get("idea")
    Idea.send_idea(idea, session["id"])
    return redirect('/ideas')

@app.route('/user/<num>', methods=['GET'])
def user_ideas(num):
    user = Usuario.select_user(num)
    user = user[0]
    ideas = Idea.user_idea(num)
    return render_template("user.html", session=session, user=user, ideas=ideas)

@app.route('/ideas/edit/<num>', methods=['GET'])
def edit_idea(num):
    idea = Idea.get_idea(num)
    return render_template('edit_idea.html', session=session, idea=idea)

@app.route('/ideas/edit/<num>/send', methods=['POST'])
def edit_idea_send(num):
    idea = request.form.get("idea")
    Idea.edit_idea(idea, num)
    return redirect('/ideas')

@app.route('/ideas/delete/<num>', methods=['GET'])
def delete_idea(num):
    Idea.del_idea(num)
    return redirect('/ideas')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear
    return redirect('/')

    


if __name__ == '__main__':
    app.run(debug=True)