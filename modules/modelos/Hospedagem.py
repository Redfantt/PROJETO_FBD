class Hospedagem(object):
    def __init__(self,id_funcionario,id_cliente,id_quarto,data_entrada,data_saida,valor_entrada,valor_total,status):
        self.__id = None
        self.__id_funcionario = id_funcionario
        self.__id_cliente = id_cliente
        self.__id_quarto = id_quarto
        self.__data_entrada = data_entrada
        self.__data_saida = data_saida
        self.__valor_entrada = valor_entrada
        self.__valor_total = valor_total
        self.__status = status

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def jsonHospedagem(self):
        return dict(
            id_funcionario = self.__id_funcionario,
            id_cliente = self.__id_cliente,
            id_quarto = self.__id_quarto,
            data_entrada = self.__data_entrada,
            data_saida = self.__data_saida,
            valor_entrada = self.__valor_entrada,
            valor_total = self.__valor_total,
            status = self.__status
        )