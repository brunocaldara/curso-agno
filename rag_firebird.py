import json
import time
from datetime import datetime
from pydoc import text
from tracemalloc import start

import firebird.driver as fdb
import ollama
import psycopg


def main():
    start_time_script = datetime.now()

    try:
        con_fb = fdb.connect(
            database='localhost:/opt/firebird/examples/empbuild/dolphins.FDB',
            user='sysdba',
            password='masterkey',
            charset='UTF-8',
        )

        cur_fb = con_fb.cursor()

        con_pg = psycopg.connect(
            host='localhost',
            port=5433,
            dbname='megaonline',
            user='postgres',
            password='password'
        )

        cur_pg = con_pg.cursor()

        cur_fb.execute(
            'SELECT FIRST 1 PRODUTOCODIGO AS id, PRODUTONOME as name FROM PRODUTO')
        products = cur_fb.fetchall()

        for product in products:
            id = product[0]
            name = str(product[1]).replace('\x00', '')
            new_product = {
                'id': id,
                'name': name
            }

            response = ollama.embed(
                model='nomic-embed-text',
                input=name
            )
            print(response['embeddings'][0])

            # print(new_product)
            # print(name)
            # print(product)
            # cur_pg.execute(
            #     "INSERT INTO produto (id, name, item_data) VALUES (%s, %s, %s)",
            #     (id, name, json.dumps(new_product))
            # )

        con_pg.commit()

        print(len(products))
        con_fb.close()
        con_pg.close()

        end_time_script = datetime.now()

        formatted_time = formatted_time = time.strftime('%H:%M:%S', time.gmtime(
            (end_time_script - start_time_script).total_seconds()))
        print(f'Execution time: {formatted_time}')
    except Exception as e:
        print("Erro:", e)


if __name__ == "__main__":
    main()
