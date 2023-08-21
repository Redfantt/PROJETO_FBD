from re import S
import modules

conn = None
cur = None


class CreateTables:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    def criarTabelas(self):
        comandos = ("""
            CREATE TABLE IF NOT EXISTS Funcionario(
            id serial primary key not null,
            nome_funcionario VARCHAR(255) not null,
            cpf_funcionario	VARCHAR(11) not null,
            login VARCHAR(255) not null,
            senha VARCHAR(255) not null,
            status boolean not null
            )
            """,
                    """
                    CREATE TABLE IF NOT EXISTS Cliente(
                    id serial primary key not null,
                    nome_cliente VARCHAR(255) not null,
                    cpf_cliente VARCHAR(255) not null,
                    telefone_cliente VARCHAR(11) not null
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Consumo(
                    id serial primary key not null,
                    valor_total NUMERIC not null
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Quarto(
                    id serial primary key not null,
                    id_consumo INTEGER REFERENCES consumo(id),
                    num_quarto INTEGER not null,
                    num_camas INTEGER not null,
                    num_banheiros INTEGER not null,
                    diaria NUMERIC not null,
                    status boolean not null
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Hospedagem(
                    id serial primary key not null,
                    id_funcionario INTEGER REFERENCES funcionario(id) not null,
                    id_cliente INTEGER REFERENCES cliente(id) not null,
                    id_quarto INTEGER REFERENCES quarto(id) not null,
                    data_entrada VARCHAR(255) not null,
                    data_saida VARCHAR(255),
                    valor_entrada NUMERIC not null,
                    valor_total NUMERIC not null,
                    status VARCHAR(255) not null
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Item(
                    id serial primary key not null,
                    item VARCHAR(255) not null,
                    valor_item NUMERIC not null
                    )
                    """
                    )

        for comando in comandos:
            cur.execute(comando)

        cur.close()
        conn.commit()
        conn.close()