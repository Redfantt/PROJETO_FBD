from flask import Blueprint, render_template, request, flash
from modules.blueprints import loginController
import modules.dao as dao
import modules.modelos as modelo
from flask_paginate import Pagination, get_page_args

item_page = Blueprint('item_page', __name__)


@item_page.route('/itemManager', methods=['GET', 'POST'])
def itemManager():
    if (loginController.flagLogin):
        if request.method == 'POST':
            ##adicionando item
            if request.form['button'] == "10":
                nome = request.form["getNome"]
                valor = request.form["getValor"]
                dao.ItemDAO().adicionarItem(modelo.Item(nome, valor))
            ##remover item
            elif request.form['button'] == "11":
                id = request.form["getId"]
                dao.ItemDAO().removerItemBanco(id)

        # Aréa Paginação
        qtdItems = list(range(int(len(dao.ItemDAO().buscarTodosItens()))))
        items = dao.ItemDAO().buscarTodosItens()

        def get_items(offset=0, per_page=10):
            return qtdItems[offset: offset + per_page]

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination_items = get_items(offset=offset, per_page=per_page)
        total = len(qtdItems)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template("item.html", items=pagination_items, page=page, per_page=50, pagination=pagination,
                               dezitems=items)

    else:
        return "<h1>Não Conectado ao Sistema,faça o login.</h1>"


