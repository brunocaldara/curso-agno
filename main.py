from agno.agent import Agent
# from agno.db.sqlite import SqliteDb
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from dotenv import load_dotenv

# from agno.tools.workspace import Workspace

load_dotenv()

# Read a Markdown file as plain text


def read_markdown_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


db = PostgresDb(
    db_url="postgresql://postgres:password@localhost:5432/curso_agno")

md_instructions = read_markdown_file("instructions.md")

workbench = Agent(
    name="Nina - Megamix Comercial",
    # model=OpenAIResponses(id="gpt-5.2"),
    model=OpenAIResponses(id="gpt-5.4-mini"),
    instructions=md_instructions,
    # db=SqliteDb(db_file="workbench.db"),  # session storage
    db=db,                                 # session storage
    # tools=[Workspace(".")],               # operate in this directory
    enable_agentic_memory=True,           # remembers across sessions
    add_history_to_context=True,          # add past runs to context
    num_history_runs=3,                   # last 3 runs
    session_id="nina-megamix-comercial",
    enable_user_memories=True,
    add_memories_to_context=True,
    add_knowledge_to_context=True,
    debug_mode=True,
    markdown=True
)

# Serve via AgentOS, get streaming, auth, session isolation, API endpoints
agent_os = AgentOS(agents=[workbench], tracing=True)
app = agent_os.get_app()
