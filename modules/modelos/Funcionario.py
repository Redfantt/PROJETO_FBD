class Funcionario(object):
    def __init__(self,nome,cpf,login,senha,status):
        self.__id = None
        self.__nome = nome
        self.__cpf = cpf
        self.__login = login
        self.__senha = senha
        self.__status = status

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def jsonFuncionario(self):
        return dict(
            nome_funcionario = self.__nome,
            cpf_funcionario = self.__cpf,
            login = self.__login,
            senha = self.__senha,
            status = self.__status
        )
