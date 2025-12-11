import httpx
from pathlib import Path
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.csv_toolkit import CsvTools

load_dotenv()

# -----------------------------------------------------
# 1. Baixa automaticamente o arquivo IMDB da documentação
# -----------------------------------------------------
url = "https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
response = httpx.get(url)

imdb_csv = Path(__file__).parent.joinpath("wip").joinpath("imdb.csv")
imdb_csv.parent.mkdir(parents=True, exist_ok=True)
imdb_csv.write_bytes(response.content)

# -----------------------------------------------------
# 2. Criação do agente com CSV Tools + Groq
# -----------------------------------------------------
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[CsvTools(csvs=[imdb_csv])],
    markdown=True,

    # -------------------------------------------------
    # 3. Instruções específicas para CONSULTAS DE FILMES
    # -------------------------------------------------
    instructions=[
        "Sempre comece listando os arquivos disponíveis.",
        "Depois verifique as colunas do arquivo IMDB.",
        "Em seguida, formule a consulta SQL necessária usando DuckDB.",
        "Sempre coloque nomes de colunas entre aspas duplas.",
        "Sempre escape aspas dentro de JSON usando \\\".",
        "Use aspas simples para valores texto.",
        "",
        "Algumas colunas importantes no arquivo IMDB incluem:",
        '"Title", "Genre", "Director", "Actors", "Year", "Rating", "Votes", "Revenue (Millions)" e "Runtime (Minutes)".',
        "",
        "Quando perguntado sobre filmes, produza a consulta exata, execute e forneça resultados claros.",
        "Quando perguntado sobre rankings, ordene adequadamente (ex: maior rating primeiro).",
        "Quando perguntado sobre estatísticas, use funções como COUNT, AVG, MAX ou SUM.",
    ],
)

# -----------------------------------------------------
# 4. Executa o agente no terminal (CLI)
# -----------------------------------------------------
if __name__ == "__main__":
    agent.cli_app(stream=False)
