import modules
import modules.dao as dao

conn = None
cur = None


class ConsumoDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def adicionarConsumo(consumo):
        valor_total = consumo.jsonConsumo()["valor_total"]
        cur.execute(f"INSERT INTO consumo(valor_total) values({valor_total}) returning id")
        idConsumo = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        conn.close()

        return idConsumo

    # Join Buscando
    @staticmethod
    def buscarConsumoEmQuarto(quarto):
        idConsumo = dao.QuartoDAO().buscarQuartoBanco(quarto)["id_consumo"]
        valorAtual = 0

        cur.execute(
            f"select valor_total from quarto INNER JOIN consumo ON quarto.id_consumo = consumo.id where quarto.id_consumo = {idConsumo}")
        valorAtual += cur.fetchall()[0][0]

        conn.commit()
        cur.close()
        conn.close()

        return valorAtual, idConsumo

    @staticmethod
    def buscarConsumo(id):
        if ConsumoDAO.validarConsumo(id):
            cur.execute(f"SELECT * FROM consumo WHERE id = '{id}'")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                valor_total=array[0][1]

            )
        else:
            return "Não encontrado!"

    @staticmethod
    def buscarTodosCosumo():
        cur.execute("SELECT * FROM consumo")
        array = cur.fetchall()

        dados = list()

        if (len(array) != 0):
            for index, quarto in enumerate(array):
                dados.append(dict(
                    id=quarto[0],
                    valor_total=quarto[1],
                ))

            return dados

        else:
            return "Não Existem consumo na base"

    @staticmethod
    def validarConsumo(id_consumo):
        cur.execute(f"select id from consumo where id = {id_consumo}")
        array = cur.fetchall()

        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def alterarConsumo(idConsumo, novoValor):
        if (ConsumoDAO.validarConsumo(idConsumo)):
            cur.execute(
                f"UPDATE consumo SET valor_total={novoValor} WHERE id={idConsumo}")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def removerConsumo(id):
        if (ConsumoDAO.validarConsumo(id)):
            cur.execute(f"DELETE FROM quarto  WHERE id = '{id}'")
            conn.commit()
            cur.close()
            conn.close()

        else:
            return "Consumo não encontrado!"