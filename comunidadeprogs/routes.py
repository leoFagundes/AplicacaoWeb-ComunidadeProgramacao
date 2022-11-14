from flask import render_template, url_for, request, flash, redirect, abort
from comunidadeprogs import app, database, bcrypt
from comunidadeprogs.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadeprogs.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image #pip install Pillow

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id).all()
    posts = posts[::-1]
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

# methods=['GET', 'POST'] serve para liberar os métodos get e posts nessa função
@app.route('/Login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarConta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            #fez login com sucesso
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', "alert-success")
            par_next = request.args.get('next') #vai pegar o argumento no 'next' que tem na URL caso exista
            if par_next:
                return redirect(par_next) #se o parâmentro next existir ai ele vai redirecionar para a página com o valor do next
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.', "alert-danger")
    if form_criarConta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarConta.senha.data)
        #criar o Usuario
        usuario = Usuario(username=form_criarConta.username.data, email=form_criarConta.email.data, senha=senha_cript)
        #adicionar session
        database.session.add(usuario)
        #commitar session
        database.session.commit()
        #criou a conta com sucesso
        flash(f'Conta criada para o e-mail: {form_criarConta.email.data}', "alert-success")
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarConta=form_criarConta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', "alert-success")
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) #vai pegar a imagem do usuáriuo que por padrão é default.jpg definido em models.py
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    #adicionar um codigo aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao

    #reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # salvar a imagem na pasta fotos_perfil
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    imagem_reduzida.save(caminho_completo)

    return nome_arquivo

def atualizar_linguagens(form):
    lista_linguagens = []
    for campo in form:
        if 'linguagem_' in campo.name:
            if campo.data:
                #adicionar o texto do campo.label (python...) na lista de linguagens
                lista_linguagens.append(campo.label.text)
    return ';'.join(lista_linguagens)

'''
Cola para verificar no banco de dados pelo Python console:
----------------------------------------
from comunidadeprogs import database
from comunidadeprogs.models import Usuario

usuario = Usuario.query.filter_by(email='leoTeste@gmail.com').first()

usuario.linguagens

'''

def bool_editar_perfil(form, lista):
    for item in lista:
        if item == "Python":
            form.linguagem_python.data = True
        if item == "c++":
            form.linguagem_cplus.data = True
        if item == "c#":
            form.linguagem_csharp.data = True
        if item == "Java":
            form.linguagem_java.data = True
        if item == "SQL":
            form.linguagem_sql.data = True
        if item == "JavaScript":
            form.linguagem_javascript.data = True
        if item == "R":
            form.linguagem_r.data = True
        if item == "HTML/CSS":
            form.linguagem_htmlcss.data = True
        if item == "TypeScript":
            form.linguagem_typescript.data = True
        if item == "PHP":
            form.linguagem_php.data = True
        if item == "Shell":
            form.linguagem_shell.data = True
        if item == "Ruby":
            form.linguagem_ruby.data = True
        if item == "Assembly":
            form.linguagem_assembly.data = True
        if item == "Swift":
            form.linguagem_swift.data = True
        if item == "Go":
            form.linguagem_go.data = True


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    print(current_user.linguagens)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            #mudar o campo foto_perfil do usuario para o novo nome da imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.linguagens = atualizar_linguagens(form)
        database.session.commit()
        flash(f'Perfil atualizado com Sucesso', "alert-success")
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        bool_editar_perfil(form, current_user.linguagens.split(';'))
        
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado', 'alert-success')
            return redirect(url_for("home"))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)