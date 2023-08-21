class Consumo(object):
    def __init__(self,valor_total):
        self.__id = None
        self.__valor_total = valor_total

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def jsonConsumo(self):
        return dict(
            valor_total=self.__valor_total
        )