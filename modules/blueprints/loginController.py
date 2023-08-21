from flask import Blueprint, render_template, request, redirect, url_for
import modules.dao as dao

login_page = Blueprint('login_page', __name__)

flagLogin = False
usuario = None


@login_page.route('/login/', methods=['GET', 'POST'])
def login():
    global flagLogin
    global usuario

    if request.method == 'POST':
        usuario = request.form["getLogin"]
        senha = request.form["getPassword"]

        validar = dao.FuncionarioDAO().buscarFuncionarioBancoLogin(usuario, senha)

        if validar:
            flagLogin = True
            return redirect(url_for('login_page.logado'))

        else:
            return render_template("login.html")

    else:
        return render_template("login.html")


@login_page.route("/logado/")
def logado():
    if (flagLogin == True):
        dao.FuncionarioDAO().alterarFuncionarioStatus(usuario, 'true')
        return render_template("logado.html")
    else:
        return "<h1>Não Conectado ao Sistema,faça o login.</h1>"