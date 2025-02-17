from dotenv import load_dotenv

from agent.copy_generator import CopyGenerator
from agent.supervisor import Supervisor
from agent.web_searcher import WebSearcher
from models.grounding_llm import GroundingLLM
from models.llm import LLM

load_dotenv()

llm = LLM(model_name="gemini", temperature=0.5)
grounding_llm = GroundingLLM()

copy_generator = CopyGenerator(llm)
web_searcher = WebSearcher(grounding_llm)
supervisor = Supervisor(llm, copy_generator, web_searcher)


user_input = input("Please enter a message: ")
inputs = {"messages": user_input}
config = {"configurable": {"thread_id": "1"}}

supervisor.write_mermaid_graph(supervisor.graph)

for event in supervisor.graph.stream(
    inputs, config, stream_mode="values", subgraphs=True
):
    print(event)
