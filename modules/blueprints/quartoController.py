from flask import Blueprint, render_template, request
from modules.blueprints import loginController
import modules.dao as dao
import modules.modelos as modelo
from flask_paginate import Pagination, get_page_args

quarto_page = Blueprint('quarto_page', __name__)


@quarto_page.route("/quartoManager", methods=["GET", "POST"])
def quartoManager():
    if (loginController.flagLogin):
        if request.method == 'POST':
            ##adicionando quarto
            if request.form['button'] == "10":
                numQuarto = request.form["getNumero"]
                qtdCamas = request.form["getCama"]
                qtdBanheiro = request.form["getBanheiro"]
                diaria = request.form["getDiaria"]

                dao.QuartoDAO().adicionarQuarto(
                    modelo.Quarto(numQuarto, 'null', qtdCamas, qtdBanheiro, 'false', diaria))
            ##ocupar quarto
            if request.form['button'] == "11":
                cliente = request.form["getCliente"]
                quarto = request.form["getQuarto"]

                if (dao.QuartoDAO().validarQuarto(quarto)) and (dao.ClienteDAO().validarCPF(cliente)):
                    ocupado = dao.QuartoDAO().buscarQuartoBanco(quarto)

                    if not ocupado['status']:
                        dao.QuartoDAO().ocuparQuarto(quarto)

                    else:
                        print('Quarto Ocupado')

                else:
                    pass
            ##adicionar consum ao quarto
            if request.form['button'] == "12":
                quarto = request.form["getQuartoConsumir"]
                itemNome = request.form["getItem"]
                quantidade = request.form["getQuantidade"]

                if ((dao.QuartoDAO().validarQuarto(quarto)) and (dao.ItemDAO().buscarItemNome(itemNome) != False)):
                    if (dao.QuartoDAO().buscarQuartoBanco(quarto)["status"] != False):
                        valorAtual, idConsumir = dao.ConsumoDAO().buscarConsumoEmQuarto(quarto)

                        item = dao.ItemDAO().buscarItemNome(itemNome)["valor_item"]
                        valorProximo = float(valorAtual) + (float(item) * float(quantidade))

                        dao.ConsumoDAO().alterarConsumo(idConsumir, float("{:.2f}".format(valorProximo)))

        # Aréa Paginação
        qtdQuartos = list(range(int(len(dao.QuartoDAO().buscarTodosQuartos()))))
        quartos = dao.QuartoDAO().buscarTodosQuartos()
        consumo = dao.ConsumoDAO().buscarTodosCosumo()

        def get_quartos(offset=0, per_page=10):
            return qtdQuartos[offset: offset + per_page]

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination_quartos = get_quartos(offset=offset, per_page=per_page)
        total = len(qtdQuartos)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template("quarto.html", quartos=pagination_quartos, page=page, per_page=50, pagination=pagination,
                               dezquartos=quartos, consumos=consumo)

    else:
        return "<h1>Não Conectado ao Sistema,faça o login.</h1>"
