from flask import render_template, url_for, redirect, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import CriarConta, Login, EditarPerfil, FormCriarPost, FormEditarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image




@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("home.html", posts=posts)


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    login = Login()
    criar_conta = CriarConta()

    if login.validate_on_submit() and "submit_button_login" in request.form:
        usuario = Usuario.query.filter_by(email=login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, login.password.data):
            login_user(usuario, remember=login.remember_data.data)
            flash(f"Login Feito com Sucesso no Email {login.email.data}", "alert-success")
            par_next = request.args.get("next")
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for("homepage"))
        else:
            flash("Falha no Login, E-mail ou senha incorretos", "alert-danger")
    if criar_conta.validate_on_submit() and "submit_button" in request.form:
        cript_pass = bcrypt.generate_password_hash(criar_conta.password.data)
        usuario = Usuario(
            username=criar_conta.username.data,
            email=criar_conta.email.data,
            password=cript_pass
        )
        database.session.add(usuario)
        database.session.commit()

        flash("Conta Criada com Sucesso!", "alert-success")
        return redirect(url_for("homepage"))

    return render_template("login.html", login=login, criar_conta=criar_conta)



@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout Feito com Sucesso!", "alert-success")
    return redirect(url_for("homepage"))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename="fotos_perfil/{}".format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)


@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(
            title=form_criar_post.title.data,
            corpo=form_criar_post.body.data,
            autor=current_user
        )
        database.session.add(post)
        database.session.commit()
        flash("Post Criado com Sucesso!", "alert-success")
        return redirect(url_for("homepage"))
    return render_template("criarpost.html", form_criar_post=form_criar_post)


def save_image(imagem):
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + cod + extensao
    caminho_completo = os.path.join(app.root_path, "static/fotos_perfil", nome_arquivo)
    tamanho= (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)   
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form_editar_perfil):
    lista_cursos = []
    for campo in form_editar_perfil:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ";".join(lista_cursos)
    


@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form_editar_perfil = EditarPerfil()
    if form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        if form_editar_perfil.foto_perfil.data:
            name_image = save_image(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = name_image
        current_user.cursos = atualizar_cursos(form_editar_perfil)
        database.session.commit()
        flash("Perfil Atualizado com Sucesso", "alert-success")
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form_editar_perfil.email.data = current_user.email
        form_editar_perfil.username.data = current_user.username

    foto_perfil = url_for('static', filename="fotos_perfil/{}".format(current_user.foto_perfil))
    return render_template("editarperfil.html", foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)


@app.route("/post/<post_id>", methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editar_post = FormEditarPost()
        if request.method == "GET":
            form_editar_post.title.data = post.title
            form_editar_post.body.data = post.corpo
        elif form_editar_post.validate_on_submit():
            post.title = form_editar_post.title.data
            post.corpo = form_editar_post.body.data
            database.session.commit()
            flash("Post Editado com Sucesso", "alert-success")
            return redirect(url_for("homepage"))
    else:
        form_editar_post = None
    return render_template("post.html", post=post, form_editar_post=form_editar_post)


@app.route("/post/<post_id>/excluir", methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post Excluido com Sucesso", "alert-danger")
        return redirect(url_for("homepage"))
    else:
        abort(403)