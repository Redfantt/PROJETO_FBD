from flask import Flask,redirect,url_for
import modules.blueprints as blue

app = Flask(__name__)

@app.route("/")
def hello_world():
     return redirect(url_for("login_page.login"))


#Registrando BluePrints
app.register_blueprint(blue.login_page)
app.register_blueprint(blue.logoff_page)
app.register_blueprint(blue.cliente_page)
app.register_blueprint(blue.quarto_page)
app.register_blueprint(blue.item_page)
app.register_blueprint(blue.hospedagem_page)

