from flask import Blueprint, redirect, url_for
from modules.blueprints import loginController
import modules.dao as dao

logoff_page = Blueprint('logoff_page', __name__)


@logoff_page.route("/logoff", methods=["GET", "POST"])
def realizarLogoff():
    loginController.flagLogin = False
    dao.FuncionarioDAO().alterarFuncionarioStatus(loginController.usuario, 'false')
    return redirect(url_for('login_page.login'))
