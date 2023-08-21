from distutils.util import execute
import modules
import modules.dao as dao
from datetime import date

conn = None
cur = None


class HospedagemDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def adicionarHospedagem(hospedagem):
        id_funcionario, id_cliente, id_quarto, data_entrada, data_saida, valor_entrada, valor_total, status = hospedagem.jsonHospedagem().values()
        cur.execute(
            f"INSERT INTO hospedagem(id_funcionario,id_cliente,id_quarto,data_entrada,data_saida,valor_entrada,valor_total,status) values({id_funcionario},{id_cliente},{id_quarto},'{data_entrada}','{data_saida}',{valor_entrada},{valor_total},'{status}')"
        )

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscarHospedagem(id):
        if (HospedagemDAO.validarHospedagem(id)):
            cur.execute(f"SELECT * FROM hospedagem WHERE id = '{id}'")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                id_funcionario=array[0][1],
                id_cliente=array[0][2],
                id_quarto=array[0][3],
                data_entrada=array[0][4],
                data_saida=array[0][5],
                valor_entrada=array[0][6],
                valor_total=array[0][7],
                status=array[0][8]
            )

        else:
            return "Não encontrado!"

    @staticmethod
    def buscarHospedagemQuarto(num_quarto):
        cur.execute(f"""
        SELECT 	hospedagem.id,
		        num_quarto

        from hospedagem

        INNER JOIN quarto
	        ON quarto.id = hospedagem.id_quarto	
        WHERE num_quarto = {num_quarto}
        ORDER BY id DESC
        """)
        array = cur.fetchall()

        if len(array) > 0:
            return True, array[0][0]

        return False

    @staticmethod
    def buscarTodasHospedagem():
        cur.execute("SELECT * FROM hospedagem")
        array = cur.fetchall()

        dados = list()

        if (len(array) != 0):
            for index, quarto in enumerate(array):
                dados.append(dict(
                    id=array[0][0],
                    id_funcionario=array[index][1],
                    id_cliente=array[index][2],
                    id_quarto=array[index][3],
                    data_entrada=array[index][4],
                    data_saida=array[index][5],
                    valor_entrada=array[index][6],
                    valor_total=array[index][7],
                    status=array[index][8]
                ))

            return dados

        else:
            return "Não Existem hospedagens na base"

    @staticmethod
    def buscarTodasHospedagensFormatadas():
        cur.execute("""
        SELECT
	quarto.num_quarto,
	funcionario.nome_funcionario,
	cliente.nome_cliente,
	hospedagem.data_entrada,
	hospedagem.data_saida,
	quarto.diaria,
	consumo.valor_total,
	quarto.diaria + consumo.valor_total,
    hospedagem.status,
    hospedagem.valor_entrada
    FROM hospedagem

    INNER JOIN funcionario
	    ON hospedagem.id_funcionario = funcionario.id
    INNER JOIN cliente
	    ON hospedagem.id_cliente = cliente.id
    INNER JOIN quarto
	    ON hospedagem.id_quarto = quarto.id
    INNER JOIN consumo
	    ON quarto.id_consumo = consumo.id
    WHERE hospedagem.status = 'Aberto'
        """)

        array = cur.fetchall()

        dados = list()

        if (len(array) != 0):
            for index, quarto in enumerate(array):
                dados.append(dict(
                    num_quarto=array[index][0],
                    nome_funcionario=array[index][1],
                    nome_cliente=array[index][2],
                    data_entrada=array[index][3],
                    data_saida=array[index][4],
                    diaria=array[index][5],
                    valor_consumido=array[index][6],
                    soma_total=array[index][7],
                    status=array[index][8],
                    valor_entrada=array[index][9]
                ))

            return dados

        else:
            return []

    @staticmethod
    def quitarHospedagem(idHosp, quarto):
        today = date.today()
        dataHoje = today.strftime("%d/%m/%Y")
        dao.QuartoDAO().desocuparQuarto(quarto)

        cur.execute(f"""
        UPDATE hospedagem
        SET data_saida = '{dataHoje}',
            status = 'Pago'
        WHERE id = {idHosp}
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def removerHospedagem(id):
        if HospedagemDAO.validarHospedagem(id):
            cur.execute(f"DELETE FROM hospedagem  WHERE id = '{id}'")
            conn.commit()
            cur.close()
            conn.close()

        else:
            return "Hospedagem não encontrado!"