import os
from dotenv import load_dotenv
from typing import Literal
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task as lg_task
from pydantic import SecretStr
from pydantic_core import ValidationError

from src.contracts import AgentTask, AgentResult

load_dotenv()

def run_test_gen_agent(task: AgentTask) -> AgentResult:
    """
    Acesta este nodul specialist pentru S5.
    Primeste un AgentTask, apeleaza Mistral folosind Structured Outputs
    si returneaza un AgentResult complet populat dinamic de model in functe de ce se cere.
    Limbajul tinta vine din task.context, pre populat de orchestrator, nu din input payload.
    """

   

    api_key: SecretStr = SecretStr(result if (result := os.environ.get("MISTRAL_API_KEY")) is not None else "")
    if not api_key:
        raise ValueError("lipseste MISTRAL_APIKEY in variabilele de mediu")
    
    try:
        llm = ChatMistralAI(model_name="mistral-small-latest", api_key = api_key, temperature=0.2)
        structured_llm = llm.with_structured_output(AgentResult)
    except Exception as e:
        raise RuntimeError(f"{e}")
    


    payload = task.input_payload or {}
    context =  task.context or {}

    language = context.get("language", "csharp")
    module_name = payload.get("module_name", "modul necunoscut")
    criteria = payload.get("acceptance_criteria", [])

    system_prompt = getPrompt("system", {"language": language})
    user_prompt = getPrompt("user", {"module_name": module_name, "criteria": criteria, "language": language, "context": context})

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    try:
        result = structured_llm.invoke(messages)
    except ValidationError as e:
        raise RuntimeError(f"Validarea AgentResult a eșuat: {e}")

    if not isinstance(result, AgentResult):
        raise RuntimeError(f"Modelul nu a returnat un AgentResult valid. Tipul returnat: {type(result)}")
    
    result = result.model_copy(update={"task_id": task.task_id, "agent_id": "S5"})

    return result

def getPrompt(type: Literal["system", "user"], options: dict) -> str:
    switch = {
        "system": getSystemPrompt,
        "user": getUserPrompt
    }
    return switch.get(type, getSystemPrompt)(**options)

def getSystemPrompt(language: str) -> str:
       return f"""
        Ești Test Engineer (Agentul S5). Limbajul țintă pentru acest task este: {language}.
        Folosește EXCLUSIV framework-ul de test și convențiile din playbook-ul de mai jos —
        nu introduce sintaxă din alt limbaj sau alt framework.
        Inainte sa returnezi rezultatul, verifica-ti singur codul: are fiecare test cel putin un [Trait(\"Category\", \"...\")]?
        Are fiecare test un comentariu // vault_ref? Daca nu, adauga-le inainte de a raspunde
    
        Trebuie să completezi TOATE câmpurile schemei AgentResult, inclusiv:
        - artifacts: o listă cu exact un Artifact, al cărui `content` este codul de test complet
        pentru limbajul {language}, iar `requires_approval=True`.
        - confidence: 0.8-0.95 dacă acceptance criteria erau clare și ai găsit note relevante în vault;
        0.5-0.79 dacă a lipsit context sau criteriile erau ambigue;
        <0.5 dacă ai fost nevoit să presupui ceva esențial.
        - rationale: motivează explicit DE CE ai ales acel nivel de confidence.
        - reasoning_chain: pașii reali pe care i-ai urmat pentru acest task specific.
        - evidence_class: "retrieved" (design bazat pe vault), NU "measured".
        - status: "success" dacă ai reușit, altfel "failed" sau "pending_approval".
        """


def getUserPrompt(module_name: str, criteria: list[str], language: str, context: str) -> str:
    return f"""
    Genereaza teste in pytest pentru modulul '{module_name}' 
    cu urmatoarele criterii de acceptare: {criteria}.
    Reguli si capcane specifice extrase din Second Brain:\n{context}
    """