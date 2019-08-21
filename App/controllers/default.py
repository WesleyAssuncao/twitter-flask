# Rota da pagina
from flask import render_template, flash, redirect, url_for,request
from flask_login import login_user, logout_user
from App import app, db, lm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

from App.models.table import User,Post
from App.models.forms import LoginForm, CadastroForm, postarForm


# Rota da pagina index (página inicial)
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

#-----------------------------x--------------------------------------------------------#

# Rota da pagina de login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            return redirect(url_for("conteudo"))
        else:
            flash("Invalid login.")
    return render_template('login.html',form=form)

#-----------------------------x---------------------------------------------------------#

# Rota da página Logout (usuário)
@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

#-----------------------------x----------------------------------------------------------#

# Rota da página cadastrar usúario  (usuário)
@app.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():
    form_cadastro_usuario = CadastroForm()

    username = None
    password = None
    name = None
    email = None

    if request.method == "POST":
          username = request.form.get("username")
          password = request.form.get("password")
          name = request.form.get("name")
          email = request.form.get("email")

    if username and password and name and email:
          p =  User(username, password, name, email)
          db.session.add(p)
          db.session.commit()
          flash('Usuario cadastrado com sucesso')

    return render_template('cadastro_usuario.html',
                          form_cadastro_usuario=form_cadastro_usuario)

#-----------------------------x-------------------------------------------------------------#


# Rota da página de lista (usuário)
@app.route("/lista")
def lista():
    Users = User.query.all()
    return render_template('lista.html', Users=Users)

#-----------------------------x--------------------------------------------------------------#

# Rota da página deletar (usuário)
@app.route("/excluir/<int:id>")
def excluir(id):
    userd = User.query.filter_by(id=id).first()

    db.session.delete(userd)
    db.session.commit()
    flash('Usuario deletado com sucesso')

    Users = User.query.all()
    return render_template('lista.html', Users=Users)

#-----------------------------x---------------------------------------------------------------#

# Rota da página atualizar (usuário)
@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    form_cadastro_usuario = CadastroForm()
    userd = User.query.filter_by(id=id).first()

    username = None
    password = None
    name = None
    email = None

    if request.method == "POST":
          username = request.form.get("username")
          password = request.form.get("password")
          name = request.form.get("name")
          email = request.form.get("email")

    if username and password and name and email:
        userd.username = username
        userd.password = password
        userd.name = name
        userd.email = email

        db.session.commit()
        flash('Usuario editado com sucesso')

        return redirect(url_for("lista"))
    return render_template("atualizar.html", userd=userd, form_cadastro_usuario=form_cadastro_usuario)

#-----------------------------x-------------------------------------------------------------------------#

# Rota Conteudo da pagina - Após login
@app.route("/conteudo", methods=["GET", "POST"])
def conteudo():

    content = None
    user_id = None

    if request.method == "POST":
        content = request.form.get("content")
        user_id = request.form.get("user_id")

    if content and user_id:
            p = Post(content, user_id)
            db.session.add(p)
            db.session.commit()
            flash('Mensagem Postada com sucesso')

    Usersd = Post.query.all()
    form_conteudo = postarForm()

    return render_template('post.html',form_conteudo=form_conteudo, Usersd=Usersd)

#-----------------------------x---------------------------------------------------------------------------#

# Rota da página deletar (post)
@app.route("/deletar/<int:id>", methods=["GET", "POST"])
def deletar(id):
    userd = Post.query.filter_by(id=id).first() # Esse 1 objeto está filtrando no banco o 1 id selecionado

    db.session.delete(userd)   # deletando no banco
    db.session.commit()        # Comitando no banco
    flash('Postagem deletada com sucesso')

    return conteudo() # Retornando uma função dentro de outra função

#-----------------------------x-----------------------------------------------------------------------------#

# Rota da página atualizar (post)
@app.route("/atualpost/<int:id>", methods=['GET', 'POST'])
def atualizar_post(id):
    form_conteudo = postarForm()
    userd = Post.query.filter_by(id=id).first()

    content = None

    if request.method == "POST":
        content = request.form.get("content")

    if content:
        userd.content = content
        p = Post(content)
        db.session.add(p)
        db.session.commit()
        flash('Mensagem editado com sucesso')


        return redirect(url_for("post"))

    return render_template("atualpost.html", userd=userd, form_conteudo= form_conteudo)


