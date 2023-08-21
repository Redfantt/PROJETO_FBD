import modules
import modules.dao as dao
import modules.modelos as modelo

conn = None
cur = None


class QuartoDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def adicionarQuarto(quarto):
        num_quarto, id_consumo, num_camas, num_banheiros, status, diaria = quarto.jsonQuarto().values()

        if (QuartoDAO.validarQuarto(num_quarto)):
            print("Já existente!")
        else:
            cur.execute(
                f"INSERT INTO quarto(id_consumo,num_camas, num_banheiros, status,num_quarto, diaria) values ({id_consumo},'{num_camas}','{num_banheiros}',{status},'{num_quarto}',{diaria}) returning id")
            quarto.setId(cur.fetchone()[0])

            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def buscarQuartoBanco(numero):

        if (QuartoDAO.validarQuarto(numero)):
            cur.execute(f"SELECT * FROM quarto WHERE num_quarto = '{numero}'")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                id_consumo=array[0][1],
                num_quarto=array[0][2],
                num_camas=array[0][3],
                num_banheiros=array[0][4],
                diaria=array[0][5],
                status=array[0][6]
            )
        else:
            return False

    @staticmethod
    def buscarTodosQuartos():
        cur.execute("SELECT * FROM quarto")
        array = cur.fetchall()

        dados = list()

        if (len(array) != 0):
            for index, quarto in enumerate(array):
                dados.append(dict(
                    id=quarto[0],
                    id_consumo=quarto[1],
                    num_quarto=quarto[2],
                    num_camas=quarto[3],
                    num_banheiros=quarto[4],
                    diaria=quarto[5],
                    status=quarto[6]
                ))

            return dados

        else:
            return []

    @staticmethod
    def validarQuarto(numero):
        cur.execute(f"select num_quarto from quarto where num_quarto = {numero}")

        array = cur.fetchall()

        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def alterarQuarto(quarto):
        num_quarto, id_consumo, num_camas, num_banheiros, status, diaria = quarto.jsonQuarto().values()
        if (QuartoDAO.validarQuarto(num_quarto)):
            cur.execute(
                f"UPDATE quarto SET num_quarto='{num_quarto}',id_consumo='{id_consumo}',num_camas='{num_camas}',"
                f" num_banheiros = '{num_banheiros}', status='{status}' diaria={diaria} WHERE num_quarto = '{num_quarto}'")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def ocuparQuarto(num_quarto):
        if (QuartoDAO.validarQuarto(num_quarto)):
            id_consumo = dao.ConsumoDAO().adicionarConsumo(modelo.Consumo(0))
            cur.execute(f"UPDATE quarto SET id_consumo='{id_consumo}', status='true' WHERE num_quarto = {num_quarto}")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def desocuparQuarto(num_quarto):
        if (QuartoDAO.validarQuarto(num_quarto)):
            cur.execute(f"UPDATE quarto SET id_consumo=null, status=false WHERE num_quarto = {num_quarto}")
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def removerQuarto(numero):
        if (QuartoDAO.validarQuarto(numero)):
            cur.execute("DELETE FROM quarto  WHERE num_quarto = '{}';".format(numero))
            conn.commit()
            cur.close()
            conn.close()

        else:
            return "Quarto não encontrado!"