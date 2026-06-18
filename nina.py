from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.sql import SQLTools
from dotenv import load_dotenv

load_dotenv()

db_url = "sqlite:///megaonline.db"


def ler_arquivo_markdown(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


agent = Agent(
    model=OpenAIChat("gpt-4o-mini"),
    # instructions='Você é um assistente de banco de dados que responde a perguntas sobre o banco de dados SQLite "megaonline.db". Forneça respostas concisas e precisas com base nos dados disponíveis.',
    instructions=ler_arquivo_markdown("instructions.md"),
    tools=[SQLTools(db_url=db_url, enable_list_tables=True,
                    enable_describe_table=True, enable_run_sql_query=True)],
    debug_mode=True,
    markdown=False
)

response = agent.run("Retorne todos os produtos que são lapiseira")
print(response.content)
