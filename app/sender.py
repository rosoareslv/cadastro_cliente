from bottle import Bottle, request
import redis
import json
import psycopg2
import os


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.queue = redis.StrictRedis(host=redis_host, port=6379, db=0)
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        db_password = os.getenv('DB_PASSWORD', '123qwe')
        dsn = f'dbname={db_name} user={db_user} host={db_host} password ={db_password}'
        self.conn = psycopg2.connect(dsn)

    def register_client(self, nome, cpf, data_aniversario):
        cur = self.conn.cursor()
        SQL = 'INSERT INTO clientes (nome, cpf, dataAniversario) VALUES (%s, %s, %s)'
        cur.execute(SQL, (nome, cpf, data_aniversario))
        self.conn.commit()
        cur.close()
        msg = {'name': nome, "cpf": cpf, 'dataAniversario': data_aniversario}
        self.queue.rpush('sender', json.dumps(msg))
        print('Cliente cadastrado com sucesso!')

    def send(self):
        nome = request.forms.get("nome")
        cpf = request.forms.get("cpf")
        data_aniversario = request.forms.get("dataAniversario")
        self.register_client(nome, cpf, data_aniversario)
        return f'Cadastro do cliente com cpf {cpf} fila!'

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=7080, debug=True)
