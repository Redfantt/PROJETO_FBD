from flask import Blueprint, render_template, request
from modules.blueprints import loginController
import modules.dao as dao
import modules.modelos as modelo
from datetime import date
from flask_paginate import Pagination, get_page_args

hospedagem_page = Blueprint("hospedagem_page", __name__)


@hospedagem_page.route("/hospedagemManager", methods=["GET", "POST"])
def hospedagemManager():
    # Aréa Paginação
    qtsHospedagens = list(range(int(len(dao.HospedagemDAO().buscarTodasHospedagensFormatadas()))))
    hospedagens = dao.HospedagemDAO().buscarTodasHospedagensFormatadas()

    def get_hospedagens(offset=0, per_page=10):
        return qtsHospedagens[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_hospedagem = get_hospedagens(offset=offset, per_page=per_page)
    total = len(qtsHospedagens)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    ###################################################################################################

    if (loginController.flagLogin):
        ##cadastra cliente e quarto e faz a hospedagem
        if request.method == 'POST':
            if request.form['button'] == "10":
                nome = request.form["getNome"]
                cpf = request.form["getCPF"]
                telefone = request.form["getTelefone"]
                quarto = request.form["getQuarto"]
                diasdiaria = request.form["getDias"]

                if (dao.QuartoDAO().validarQuarto(quarto)) and (not dao.ClienteDAO().validarCPF(cpf)):
                    ocupado = dao.QuartoDAO().buscarQuartoBanco(quarto)

                    if not ocupado['status']:
                        if (int(diasdiaria) > 0):
                            # Funcionario
                            idFuncionario = dao.FuncionarioDAO().verificarFuncionarioOnline()

                            # Cliente
                            dao.ClienteDAO().adicionarClienteBanco(modelo.Cliente(nome, cpf, telefone))
                            idCliente = dao.ClienteDAO().buscarClienteNameLista(nome)[0]['id']

                            # Quarto
                            idQuarto = dao.QuartoDAO().buscarQuartoBanco(quarto)["id"]
                            dao.QuartoDAO().ocuparQuarto(quarto)

                            # Data Entrada
                            today = date.today()
                            dataHoje = today.strftime("%d/%m/%Y")

                            # Diária
                            diaria = dao.QuartoDAO().buscarQuartoBanco(quarto)["diaria"]
                            valor_total, idCon = dao.ConsumoDAO().buscarConsumoEmQuarto(quarto)

                            dao.HospedagemDAO().adicionarHospedagem(
                                modelo.Hospedagem(idFuncionario, idCliente, idQuarto, dataHoje, "00/00/0000",
                                                  diaria * int(diasdiaria), 0, "Aberto"))
                            print(hospedagens)
                            return render_template("hospedagem.html", mensagem="Quarto ocupado com sucesso",
                                                   hospedagem=pagination_hospedagem, page=page, per_page=50,
                                                   pagination=pagination, hospedagemsLista=hospedagens)
                        else:
                            return render_template("hospedagem.html", mensagem="Digite um valor maior que 0 para dias",
                                                   hospedagem=pagination_hospedagem, page=page, per_page=50,
                                                   pagination=pagination, hospedagemsLista=hospedagens)

                    else:
                        return render_template("hospedagem.html", mensagem="Quarto já está ocupado",
                                               hospedagem=pagination_hospedagem, page=page, per_page=50,
                                               pagination=pagination, hospedagemsLista=hospedagens)

                else:
                    return render_template("hospedagem.html", mensagem="Quarto já existente no banco",
                                           hospedagem=pagination_hospedagem, page=page, per_page=50,
                                           pagination=pagination, hospedagemsLista=hospedagens)
            ##quitando o quarto da hospedagem
            if request.form['button'] == "11":
                quarto = request.form["getQuartoQuitar"]

                seExiste, idHosp = dao.HospedagemDAO().buscarHospedagemQuarto(quarto)

                if seExiste:
                    dao.HospedagemDAO().quitarHospedagem(idHosp, quarto)
                    print(hospedagens)
                    return render_template("hospedagem.html", mensagem2="Quarto quitado!",
                                           hospedagem=pagination_hospedagem, page=page, per_page=50,
                                           pagination=pagination, hospedagemsLista=hospedagens)
                else:
                    return render_template("hospedagem.html", mensagem2="Quarto inválido!",
                                           hospedagem=pagination_hospedagem, page=page, per_page=50,
                                           pagination=pagination, hospedagemsLista=hospedagens)

        return render_template("hospedagem.html", hospedagem=pagination_hospedagem, page=page, per_page=50,
                               pagination=pagination, hospedagemsLista=hospedagens)

    return "<h1>Não Conectado ao Sistema,faça o login.</h1>"