class Quarto(object):
    def __init__(self,num_quarto, id_consumo,num_camas,num_banheiros,status,diaria):
        self.__id = None
        self.__num_quarto = num_quarto
        self.__id_consumo = id_consumo
        self.__num_camas = num_camas
        self.__num_banheiros = num_banheiros
        self.__status = status
        self.__diaria = diaria

    def setStatus(self, status):
        self.__status = status

    def setNumCamas(self, numeroCamas):
        self.__num_camas = numeroCamas

    def setNumeroBanheiros(self, num_banheiros):
        self.__num_banheiros = num_banheiros

    def setIdConsumo(self, id_consumo):
        self.__id_consumo = id_consumo

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def setNum(self, numero):
        self.__num_quarto = numero


    def jsonQuarto(self):
        return dict(
            num_quarto = self.__num_quarto,
            id_consumo = self.__id_consumo,
            num_camas = self.__num_camas,
            num_banheiros = self.__num_banheiros,
            status = self.__status,
            diaria = self.__diaria
        )