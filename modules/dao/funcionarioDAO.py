import modules
from modules import dao

conn = None
cur = None


class FuncionarioDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def buscarTodosFuncionarios():
        cur.execute("SELECT * FROM funcionario")
        array = cur.fetchall()

        all = dict()
        if (len(array) != 0):
            for index, funcionario in enumerate(array):
                all["Funcionario " + str(index)] = dict(
                    id=funcionario[0],
                    nome_funcionario=funcionario[1],
                    cpf_funcionario=funcionario[2],
                    login=funcionario[3],
                    senha=funcionario[4],
                    status=funcionario[5]
                )
            return all
        else:
            return "Não Existem Clientes na base"

    @staticmethod
    def buscarFuncionarioBanco(cpf):
        if (FuncionarioDAO.validarCPF(cpf)):
            cur.execute("SELECT * FROM funcionario WHERE cpf_funcionario = '{}'".format((cpf)))
            array = cur.fetchall()

            print("Nome: {}, Cpf: {}, Login: {}, Senha: {}".format(array[0][0], array[0][1], array[0][2], array[0][3]))
        else:
            print("Funcionario não encontrado")

    @staticmethod
    def buscarFuncionarioBancoLogin(login, senha):
        if (FuncionarioDAO.validarLogin(login)):
            cur.execute("SELECT * FROM funcionario WHERE login = '{}'".format((login)))
            array = cur.fetchall()

            if ((login == array[0][3]) and (senha == array[0][4])):
                return True

            return False
        else:
            return False

    @staticmethod
    def adicionarFuncionarioBanco(funcionario):
        try:
            funcDict = funcionario.jsonFuncionario()
            nome, cpf, login, senha, status = funcDict.values()
            if (FuncionarioDAO.validarCPF(cpf) == False):
                cur.execute(
                    "INSERT INTO funcionario(nome_funcionario,cpf_funcionario,login,senha,status) VALUES(%s,%s,%s,%s,%s)  returning id",
                    (nome, cpf, login, senha, status))
                funcionario.setId(cur.fetchone()[0])
                conn.commit()
                cur.close()
                conn.close()
            else:
                print("Funcionario já existente")
        except:
            pass

    @staticmethod
    def verificarFuncionarioOnline():
        cur.execute("SELECT id FROM funcionario where status = true")
        idFuncionario = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return idFuncionario[0][0]

    @staticmethod
    def validarCPF(cpf):
        cur.execute("select cpf_funcionario from funcionario where cpf_funcionario = '{}';".format(cpf))

        array = cur.fetchall()
        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def validarLogin(login):
        cur.execute("select cpf_funcionario from funcionario where login = '{}';".format(login))
        array = cur.fetchall()
        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def alterarFuncionarioStatus(login, status):
        if (dao.FuncionarioDAO().validarLogin(login)):
            cur.execute(f"UPDATE funcionario SET status='{status}' WHERE login ='{login}'")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def removerFuncionarioBanco(cpf):
        if (FuncionarioDAO.validarCPF(cpf)):
            cur.execute("DELETE FROM funcionario  WHERE cpf_funcionario = '{}';".format(cpf))
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("Funcionario não encontrado!")





