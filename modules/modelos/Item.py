class Item(object):
    def __init__(self,item,valor_item):
        self.__id = None
        self.__item = item
        self.__valor_item = valor_item

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id

    def jsonItem(self):
        return dict(
            item=self.__item,
            valor_item = self.__valor_item
        )