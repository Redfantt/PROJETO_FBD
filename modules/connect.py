import psycopg2


class Connect:
    _instance = None

    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """ Conectar a PostgreSQL database server """
        try:
            # Paramêtros
            params = dict(
                host='localhost',
                database='projetoFBDFlask',
                user='postgres',
                password='123'
            )

            # Conectando a database
            conn = psycopg2.connect(**params)

            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getConnect(self):
        return self.conn

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance