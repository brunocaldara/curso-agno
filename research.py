from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True,
    tools=[TavilyTools()],
)

agent.print_response(
    "Qual a temperatura de hoje em Cachoeiro de Itapemirim, Espírito Santo?")
