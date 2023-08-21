import modules

conn = None
cur = None


class ClienteDAO:

    def __init__(self):
        global conn
        global cur
        conn = modules.Connect().getConnect()
        cur = conn.cursor()

    @staticmethod
    def adicionarClienteBanco(cliente):

        dic_cliente = cliente.jsonCliente()
        nome, cpf, telefone = dic_cliente.values()
        if (ClienteDAO.validarCPF(cpf) == False):
            print("Entrou")
            cur.execute(
                f"INSERT INTO cliente(nome_cliente,cpf_cliente,telefone_cliente) VALUES ('{nome}','{cpf}','{telefone}') returning id")
            cliente.setId(cur.fetchone()[0])
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("Esse cliente já está cadastrado!")

    @staticmethod
    def buscarClienteName(nome):
        cur.execute(f"SELECT * FROM cliente WHERE nome_cliente  ILIKE '{nome}%';")
        array = cur.fetchall()

        all = dict()

        if (len(array) != 0):
            for index, cliente in enumerate(array):
                all[str(index + 1)] = dict(
                    id=cliente[0],
                    nome_cliente=cliente[1],
                    cpf_cliente=cliente[2],
                    telefone_cliente=cliente[3],
                )

            return all

    @staticmethod
    def buscarClienteNameLista(nome):
        cur.execute(f"SELECT * FROM cliente WHERE nome_cliente  ILIKE '{nome}%';")
        array = cur.fetchall()

        all = list()

        if (len(array) != 0):
            for index, cliente in enumerate(array):
                all.append(dict(
                    id=cliente[0],
                    nome_cliente=cliente[1],
                    cpf_cliente=cliente[2],
                    telefone_cliente=cliente[3],
                ))

            return all

    @staticmethod
    def buscarClienteBanco(cpf):
        if (ClienteDAO.validarCPF(cpf)):
            cur.execute(f"SELECT * FROM cliente WHERE cpf_cliente = '{cpf}'")
            array = cur.fetchall()

            return dict(
                id=array[0][0],
                nome_cliente=array[0][1],
                cpf_cliente=array[0][2],
                telefone_cliente=array[0][3]
            )

    @staticmethod
    def buscarTodosClientes():
        cur.execute("SELECT * FROM cliente")
        array = cur.fetchall()

        all = dict()

        if (len(array) != 0):
            for index, cliente in enumerate(array):
                all[str(index + 1)] = dict(
                    id=cliente[0],
                    nome_cliente=cliente[1],
                    cpf_cliente=cliente[2],
                    telefone_cliente=cliente[3],
                )

            return all

        else:
            return "Não Existem Clientes na base"

    @staticmethod
    def validarCPF(cpf):
        cur.execute("select cpf_cliente from cliente where cpf_cliente = '{}';".format(cpf))

        array = cur.fetchall()
        if (len(array) != 0):
            return True
        else:
            return False

    @staticmethod
    def alterarCliente(cliente, cpfOld):
        clienteDic = cliente.jsonCliente()
        nome, cpf, telefone = clienteDic.values()
        if cpfOld == cpf:
            if (ClienteDAO.validarCPF(cpf)):
                cur.execute(
                    f"UPDATE cliente SET nome_cliente='{nome}',cpf_cliente='{cpf}', telefone_cliente= '{telefone}' WHERE cpf_cliente ='{cpf}'")
                conn.commit()
                cur.close()
                conn.close()
                print("Alterado com sucesso!")
            else:
                print("cpf não encontrado")
        elif cpfOld != None and cpfOld != cpf:
            if (ClienteDAO.validarCPF(cpfOld)):
                if (ClienteDAO.validarCPF(cpf) == False):
                    cur.execute(
                        f"UPDATE cliente SET nome_cliente='{nome}',cpf_cliente='{cpf}', telefone_cliente= '{telefone}' WHERE cpf_cliente ='{cpfOld}'")
                    conn.commit()
                    cur.close()
                    conn.close()
                    print("Alterado com sucesso!")
                else:
                    print("CPF JÁ EXISTENTE")
            else:
                print("CPF Não encontrado")

        elif cpfOld == None:
            if (ClienteDAO.validarCPF(cpf)):
                cur.execute(
                    f"UPDATE cliente SET nome_cliente='{nome}',cpf_cliente='{cpf}', telefone_cliente= '{telefone}' WHERE cpf_cliente ='{cpf}'")
                conn.commit()
                cur.close()
                conn.close()
                print("Alterado com sucesso!")
            else:
                print("cpf não encontrado")

    @staticmethod
    def removerClienteBanco(cpf):
        if (ClienteDAO.validarCPF(cpf)):
            cur.execute("DELETE FROM cliente  WHERE cpf_cliente = '{}';".format(cpf))
            conn.commit()
            cur.close()
            conn.close()
            print("Removido com sucesso!")
        else:
            print("CPF não encontrado")

    @staticmethod
    def removerTudo():
        cur.execute("DELETE from cliente ")
        conn.commit()
        cur.close()
        conn.close()



