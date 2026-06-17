from agno.models.groq import Groq
from agno.models.message import Message
from agno.agent import Agent
from dotenv import load_dotenv
load_dotenv()

model = Groq(id="llama-3.3-70b-versatile")

# Mensagem do usuário
user_message = Message(role="user", content="Olá, meu nome é Rodrigo")

# Mensagem assistente
assistant_message = Message(role="assistant", content="")

# Invocar
response = model.invoke(
    messages=[user_message],
    assistant_message=assistant_message)

print(response.content)

# agent = Agent(
#     model=Groq(id="llama-3.1-8b-instant"),
#     markdown=True
# )

# # Print the response in the terminal
# agent.print_response("Share a 2 sentence horror story.")