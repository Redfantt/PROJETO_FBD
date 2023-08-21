from sys import modules
from flask import Blueprint, render_template, request, flash
from modules.blueprints import loginController
import modules.dao as dao
import modules.modelos as modelo

cliente_page = Blueprint('cliente_page', __name__)
cpf_old = None
flag = False


# Listar Todos
@cliente_page.route('/clientes', methods=['GET', 'POST'])
def clientesAll():
    if (loginController.flagLogin):

        return dao.ClienteDAO().buscarTodosClientes()
    else:

        return "<h1 font-size=10>Não Conectado ao Sistema,faça o login.</h1>"


# Buscar
@cliente_page.route('/clientes/<cpf>/', methods=['GET', 'POST'])
def clientesId(cpf):
    if (loginController.flagLogin):

        clienteReal = dao.ClienteDAO().buscarClienteBanco(cpf)
        return clienteReal

    else:
        return "<h1>Não Conectado ao Sistema,faça o login.</h1>"


@cliente_page.route("/clienteManager", methods=['GET', 'POST'])
def cadastrarCliente():
    global flag
    global cpf_old

    if (loginController.flagLogin):
        if request.method == 'POST':
            if request.form['button'] == "10":
                nome = request.form["getNome"]
                cpf = request.form["getCpf"]
                telefone = request.form["getTelefone"]

                dao.ClienteDAO().adicionarClienteBanco(modelo.Cliente(nome, cpf, telefone))
            elif request.form["button"] == "11":
                cpf = request.form["getCpf"]
                dao.ClienteDAO().removerClienteBanco(cpf)

            elif request.form["button"] == "12":
                cpf = request.form["getCpfbusca"]
                if dao.ClienteDAO().validarCPF(cpf):
                    id, nome, cpf, telefone = dao.ClienteDAO().buscarClienteBanco(cpf).values()
                    cpf_old = cpf
                    flag = True

                    return render_template("cliente.html", nomeInput=nome, cpfInput=cpf, telefoneInput=telefone)
                else:
                    pass

            elif request.form["button"] == "13":
                cpf = request.form["getCpf"]
                nome = request.form["getNome"]
                telefone = request.form["getTelefone"]
                if (flag):
                    cliente = modelo.Cliente(nome, cpf, telefone)
                    dao.ClienteDAO().alterarCliente(cliente, cpf_old)
                    flag = False
                    cpf_old = None
                else:
                    cliente = modelo.Cliente(nome, cpf, telefone)
                    dao.ClienteDAO().alterarCliente(cliente, cpf_old)

            elif request.form["button"] == "14":
                cpf = request.form["getCpf"]
                dicionario = dao.ClienteDAO().buscarClienteBanco(cpf)
                if dicionario is None:
                    return "<h1>Cliente não encontrado</h1>"

                return dicionario

            elif request.form["button"] == "15":
                nome = request.form["getNome"]
                dicionario = dao.ClienteDAO().buscarClienteName(nome)
                if dicionario is None:
                    return "<h1>Cliente não encontrado</h1>"

                return dicionario

        return render_template("cliente.html")

    else:
        return "<h1>Não Conectado ao Sistema,faça o login.</h1>"