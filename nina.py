import os
import re

import requests
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat, OpenAIResponses
from agno.os import AgentOS
from agno.tools.sql import SQLTools
from dotenv import load_dotenv
from fastapi import Body

load_dotenv()

ZPRO_API_TOKEN_NINA = os.getenv('ZPRO_API_KEY_NINA')
ZPRO_API_URL_NINA = os.getenv('ZPRO_API_URL_NINA')


db_url = "sqlite:///megaonline.db"

db = PostgresDb(
    db_url="postgresql://postgres:password@localhost:5432/curso_agno")


def ler_arquivo_markdown(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def remover_pontuacao_tool(text: str) -> str:
    '''
    Remove todos os caracteres que não são dígitos de uma string.
    Args:
        text (str): A string da qual os caracteres não numéricos serão removidos.
    Returns:
        str: A string resultante contendo apenas dígitos.
    Raises:
        TypeError: Se o argumento fornecido não for uma string.
    '''
    if not isinstance(text, str):
        raise TypeError("O valor deve ser uma string.")

    return re.sub(r'\D', '', text)


nina_comecial = Agent(
    id='nina-megamix-comercial',
    name='Nina - Megamix Comercial',
    model=OpenAIResponses('gpt-4o-mini', cache_response=True),
    instructions=ler_arquivo_markdown('instructions.md'),
    db=db,  # session storage
    tools=[SQLTools(db_url=db_url, enable_list_tables=True,
                    enable_describe_table=True, enable_run_sql_query=True),
            remover_pontuacao_tool],
    enable_agentic_memory=True,           # remembers across sessions
    add_history_to_context=True,          # add past runs to context
    num_history_runs=3,                   # last 3 runs
    session_id='nina-megamix-comercial-session',
    enable_user_memories=True,
    add_memories_to_context=True,
    add_knowledge_to_context=True,
    debug_mode=True,
    markdown=False,
)

agent_os = AgentOS(agents=[nina_comecial], tracing=True)
app = agent_os.get_app()


@app.post('/nina', tags=['Megamix Comercial'])
async def teste(body: dict = Body(...)):
    method = body.get('method')

    if method == 'message':
        ticket = body.get('ticket')
        ticket_id = ticket.get('id')
        contact = ticket.get('contact')
        number = contact['number']
        msg = body.get('msg')
        message = msg.get('message')
        conversation = message['conversation']

        print(f'Received message: {conversation}')
        print(f'From number: {number}')

        resposta = nina_comecial.run(conversation, user_id=number)
        mensagem = resposta.messages[-1]
        content = mensagem.content
        timeout = 10

        headers = {
            'Authorization': f'Bearer {ZPRO_API_TOKEN_NINA}',
            'Content-Type': 'application/json'
        }

        payload = {
            'body': content,
            'number': number,
            'externalKey': ticket_id,
            'isClosed': False

        }

        response = requests.post(
            ZPRO_API_URL_NINA, json=payload, headers=headers, timeout=timeout)

        return {'status': response.status_code}

if __name__ == "__main__":
    agent_os.serve(app='nina:app', host="0.0.0.0", port=7777, reload=True)

# response = nina_comecial.run("Retorne todos os produtos que são lapiseira")
# print(response.content)
