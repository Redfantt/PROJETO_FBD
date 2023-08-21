from flask_project.webFlask import app
import modules
import modules.dao as dao
import modules.modelos as modelo


if __name__ == '__main__':
    #Primeira Execução, evitar Bugs
    modules.CreateTables().criarTabelas()
    dao.FuncionarioDAO().adicionarFuncionarioBanco(modelo.Funcionario("Luiz Carvalho","12675203459","admin","admin",False))
    dao.FuncionarioDAO().adicionarFuncionarioBanco(modelo.Funcionario("Heldom","12675191430","123","123",False))
    dao.ItemDAO().adicionarItem(modelo.Item("Coca-Cola 2L", "7.99"))
    dao.QuartoDAO().adicionarQuarto(modelo.Quarto(101,'null',3,2,'false',20))
    
    dao.HospedagemDAO().buscarTodasHospedagensFormatadas()
    app.run(debug=True)

