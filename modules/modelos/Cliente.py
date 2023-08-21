class Cliente(object):
    def __init__(self,nome,cpf,telefone):
        self.__id = None
        self.__nome=nome
        self.__cpf = cpf
        self.__telefone = telefone

    def getId(self):
        return self.__id

    def setId(self,idC):
        self.__id = id

    def jsonCliente(self):
        return dict(
            nome_cliente = self.__nome,
            cpf_cliente = self.__cpf,
            telefone_cliente = self.__telefone,
        )