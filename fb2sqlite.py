import os
import sqlite3

import firebird.driver as fdb

SQLITE_DB_NAME = "megaonline.db"

if os.path.exists(SQLITE_DB_NAME):
    os.remove(SQLITE_DB_NAME)

con_sqlite = sqlite3.connect(SQLITE_DB_NAME)

cur_sqlite = con_sqlite.cursor()

cur_sqlite.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        preco REAL
    )
''')

con_fb = fdb.connect(
    database='localhost:/opt/firebird/examples/empbuild/dolphins.FDB',
    user='sysdba',
    password='masterkey',
    charset='UTF-8',
)

cur_fb = con_fb.cursor()

cur_fb.execute(
    'SELECT FIRST 10 PRODUTOCODIGO AS id, PRODUTONOME as nome FROM PRODUTO')

produtos = cur_fb.fetchall()

for produto in produtos:
    id = produto[0]
    nome = str(produto[1]).replace('\x00', '')
    preco = 0.0

    cur_sqlite.execute(
        "INSERT INTO produto (id, nome, preco) VALUES (?, ?, ?)", (id, nome, preco))

con_sqlite.commit()
con_sqlite.close()
con_fb.close()
