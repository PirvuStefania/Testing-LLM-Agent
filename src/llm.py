from multiprocessing import context
import os
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import SecretStr
from pydantic_core import ValidationError
from contracts import AgentResult
from dotenv import load_dotenv
from prompt import getPrompt

load_dotenv()

_structured_llm = None

def  get_structured_llm():
    global _structured_llm

    if _structured_llm is None:
        api_key: SecretStr = SecretStr(result if (result := os.environ.get("MISTRAL_API_KEY")) is not None else "")
        if not api_key:
            raise ValueError("lipseste MISTRAL_APIKEY in variabilele de mediu")

        print("creating llm client")

        try:
            llm = ChatMistralAI(model_name="mistral-small-latest", api_key = api_key, temperature=0.2, timeout=300)
            _structured_llm = llm.with_structured_output(AgentResult)
        except Exception as e:
            raise RuntimeError(f"{e}")
        
        print("llm client ready")

    return _structured_llm


def format_crew_output(task_id: str, module_name: str, criteria: list[str], vault_notes: str, crew_output: str, language: str) -> AgentResult:
    structured_llm = get_structured_llm()

    system_prompt = getPrompt("system", {"task_id": task_id})
    user_prompt = getPrompt("user", {"module_name": module_name, "criteria": criteria, "vault_notes": vault_notes, "crew_output": crew_output, "language": language})
    print(f"System prompt: {system_prompt}")
    print(f"User prompt: {user_prompt}")
    messages = [
           SystemMessage(content=system_prompt),
           HumanMessage(content=user_prompt)
       ]

    try:
        result = structured_llm.invoke(messages)
    except ValidationError as e:
        raise RuntimeError(f"AgentResult validation failed: {e}")
    
    if not isinstance(result, AgentResult):
        raise RuntimeError(f"Modelul nu a returnat un AgentResult valid. Tipul returnat: {type(result)}")
        
    result = result.model_copy(update={"task_id": task_id, "agent_id": "S5"})

    return result