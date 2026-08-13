from pathlib import Path
from crewai.project import load_crew
from crewai import LLM
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

def kickoff_content_crew(inputs: dict):
    crew, default_inputs = load_crew(Path(__file__).with_name("crew.jsonc"))

    llm = LLM(model="mistral/mistral-medium-latest")
    for agent in crew.agents:
        agent.llm = llm

    return crew.kickoff(inputs={**default_inputs, **inputs})
