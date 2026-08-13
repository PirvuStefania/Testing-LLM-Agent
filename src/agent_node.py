import os
import sys
from pathlib import Path
from contracts import AgentTask, AgentResult
from llm import format_crew_output 


from contracts import AgentTask, AgentResult

_FLOW_ROOT_ = Path(__file__).resolve().parent.parent / "s5_ai_flow" / "src"
if str(_FLOW_ROOT_) not in sys.path:
    sys.path.insert(0, str(_FLOW_ROOT_))

from s5_ai_flow.crews.content_crew.content_crew import kickoff_content_crew

def run_test_generation_agent(task: AgentTask) -> AgentResult:

    payload = task.input_payload or {}
    context =  task.context or {}

    language = context.get("language", "csharp")
    module_name = payload.get("module_name", "modul necunoscut")
    criteria = payload.get("acceptance_criteria", [])
    vault_notes = "no vault notes available yet"

    print("starting crew ai pipeline")

    try:
        crew_output = kickoff_content_crew(inputs={
            "module_name": module_name,
            "criteria": criteria,
            "vault_notes": vault_notes,
            "language": language,
        })
    except Exception as e:
        raise RuntimeError(f"Error occurred while running content crew: {e}")

    #print("crew ai pipeline finished")

    #print("formatting results into AgentResult")
    #print(crew_output.raw)
    try:
        result = format_crew_output(
            task_id=task.task_id,
            module_name=module_name,
            criteria=criteria,
            vault_notes=vault_notes,
            crew_output=crew_output.raw,
            language=language
        )
    except Exception as e:
        raise RuntimeError(f"Error formatting crew output into AgentResult: {e}")

    return result
    

