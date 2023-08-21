from re import S
import modules

conn = None
cur = None


class ItemDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def adicionarItem(item):
        nome, valor_item = item.jsonItem().values()

        cur.execute(
            f"INSERT INTO item (item,valor_item) values ('{nome}',{valor_item}) returning id")
        item.setId(cur.fetchone()[0])

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscarItem(id):
        if (ItemDAO.validarItem(id)):
            cur.execute(f"SELECT * FROM item WHERE id = '{id}'")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                item=array[0][1],
                valor_item=array[0][2]

            )
        else:
            return "Não encontrado!"

    @staticmethod
    def buscarItemNome(nome):
        if (ItemDAO.validarItemNome(nome)):
            cur.execute(f"SELECT * FROM item WHERE item  ILIKE '{nome}%';")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                item=array[0][1],
                valor_item=array[0][2]

            )
        else:
            return False

    @staticmethod
    def buscarTodosItens():
        cur.execute("SELECT * FROM item")
        array = cur.fetchall()

        dados = list()

        if (len(array) != 0):
            for index, itens in enumerate(array):
                dados.append(dict(
                    id=itens[0],
                    item=itens[1],
                    valor_item=itens[2]

                ))

            return dados

        else:
            return []

    @staticmethod
    def validarItem(id):
        cur.execute(f"select id from item where id = '{id}'")
        array = cur.fetchall()

        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def validarItemNome(nome):
        cur.execute(f"select id from item where item ILIKE '{nome}%'")
        array = cur.fetchall()

        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def alterarItemBanco(item):
        item, valor_item = item.jsonItem().values()

        if (ItemDAO.validarItem(item.getId())):
            cur.execute(
                f"UPDATE item SET item='{item}',valor_item='{valor_item}' WHERE id = '{item.getId()}'")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def removerItemBanco(id):
        if (ItemDAO.validarItem(id)):
            cur.execute(f"DELETE FROM item  WHERE id = '{id}'")
            conn.commit()
            cur.close()
            conn.close()
            print("Removido com sucesso!")

        else:
            print("Item não encontrado")