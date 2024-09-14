import redis
import json
from time import sleep
from random import randint
import os

if __name__ == "__main__":
    redis_host = os.getenv('REDIS_HOST', 'queue')
    r = redis.Redis(host=redis_host, port=6379, db=0)
    print('Aguardando clientes!!!')
    while True:
        msg = json.loads(r.blpop('sender')[1])
        print('Notificando o cliente...')
        sleep(randint(1,10))
        print(f'Cliente {msg} notificado!')
