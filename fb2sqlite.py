import os
import sqlite3
import time
from datetime import datetime

import firebird.driver as fdb

try:
    tempo_inicio_script = datetime.now()

    def criar_tabela_produto(cur_sqlite):
        cur_sqlite.execute('''
            CREATE TABLE IF NOT EXISTS produto (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                preco REAL
            )
        ''')

    def criar_tabela_cliente(cur_sqlite):
        cur_sqlite.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                cpf_cnpj TEXT
            )
        ''')

    def inserir_produtos(cur_sqlite, produtos):
        for produto in produtos:
            id = produto[0]
            nome = str(produto[1]).replace('\x00', '')
            preco = 0.0

            cur_sqlite.execute(
                "INSERT INTO produto (id, nome, preco) VALUES (?, ?, ?)", (id, nome, preco))

    def inserir_clientes(cur_sqlite, clientes):
        for cliente in clientes:
            id = cliente[0]
            nome = str(cliente[1]).replace('\x00', '')
            cpf_cnpj = str(cliente[2]).replace('\x00', '')

            cur_sqlite.execute(
                "INSERT INTO cliente (id, nome, cpf_cnpj) VALUES (?, ?, ?)", (id, nome, cpf_cnpj))

    SQLITE_DB_NAME = "megaonline.db"

    if os.path.exists(SQLITE_DB_NAME):
        os.remove(SQLITE_DB_NAME)

    con_sqlite = sqlite3.connect(SQLITE_DB_NAME)

    cur_sqlite = con_sqlite.cursor()

    criar_tabela_produto(cur_sqlite)
    criar_tabela_cliente(cur_sqlite)

    con_fb = fdb.connect(
        database='localhost:/opt/firebird/examples/empbuild/dolphins.FDB',
        user='sysdba',
        password='masterkey',
        charset='UTF-8',
    )

    cur_fb = con_fb.cursor()

    cur_fb.execute(
        'SELECT PRODUTOCODIGO AS id, PRODUTONOME as nome FROM PRODUTO')

    produtos = cur_fb.fetchall()

    inserir_produtos(cur_sqlite, produtos)

    cur_fb.execute(
        'SELECT CLIENTECODIGO AS id, CLIENTENOME as nome, CLIENTECPF as cpf_cnpj FROM CLIENTE')

    clientes = cur_fb.fetchall()

    inserir_clientes(cur_sqlite, clientes)

    con_sqlite.commit()
    con_sqlite.close()
    con_fb.close()

    tempo_fim_script = datetime.now()

    formatted_time = formatted_time = time.strftime('%H:%M:%S', time.gmtime(
        (tempo_fim_script - tempo_inicio_script).total_seconds()))
    print(f'Execution time: {formatted_time}')
except Exception as e:
    print(f"Erro: {e}")
