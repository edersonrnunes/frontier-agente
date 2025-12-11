from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os

load_dotenv()  # precisa chamar

print("DEBUG TAVILY:", os.getenv("TAVILY_API_KEY"))  # teste de diagnóstico

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools()]
    # debug_mode=True caso deseje ver o debug
)

agent.print_response(
    "use suas ferramentas para encontrar os melhores ar condicionados inverter até 2500 reais" #, stream=True para se comportar como o chatGPT, que envia linhas conforme digita
)
