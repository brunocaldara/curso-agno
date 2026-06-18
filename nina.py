from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.sql import SQLTools
from dotenv import load_dotenv

load_dotenv()

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


nina_comecial = Agent(
    name="Nina - Megamix Comercial",
    model=OpenAIChat("gpt-4o-mini"),
    instructions=ler_arquivo_markdown("instructions.md"),
    db=db,  # session storage
    tools=[SQLTools(db_url=db_url, enable_list_tables=True,
                    enable_describe_table=True, enable_run_sql_query=True)],
    enable_agentic_memory=True,           # remembers across sessions
    add_history_to_context=True,          # add past runs to context
    num_history_runs=3,                   # last 3 runs
    session_id="nina-megamix-comercial",
    enable_user_memories=True,
    add_memories_to_context=True,
    add_knowledge_to_context=True,
    debug_mode=True,
    markdown=False
)

agent_os = AgentOS(agents=[nina_comecial], tracing=True)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app='nina:app', reload=True)

# response = nina_comecial.run("Retorne todos os produtos que são lapiseira")
# print(response.content)
