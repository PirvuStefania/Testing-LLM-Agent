import enum
import os
from dotenv import load_dotenv
from typing import Dict, Any, Literal
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task as lg_task
from pydantic_core import ValidationError

from src.contracts import AgentTask, AgentResult, Artifact
from src.retriever import index_vault_notes, search_vault, load_playbook 

load_dotenv()

def run_test_gen_agent(task: AgentTask) -> AgentResult:
    """
    Acesta este nodul specialist pentru S5.
    Primeste un AgentTask, apeleaza Mistral folosind Structured Outputs
    si returneaza un AgentResult complet populat dinamic de model in functe de ce se cere.
    Limbajul tinta vine din task.context, pre populat de orchestrator, nu din input payload.
    """

    index_vault_notes()

    api_key: str = result if (result := os.environ.get("MISTRAL_API_KEY")) is not None else ""
    if not api_key:
        raise ValueError("lipseste MISTRAL_APIKEY in variabilele de mediu")
    
    try:
        llm = ChatMistralAI(model="mistral-small-latest", api_key = api_key, temperature=0.2)
        structured_llm = llm.with_structured_output(AgentResult)
    except Exception as e:
        raise RuntimeError(f"{e}")
    


    payload = task.input_payload or {}
    context =  task.context or {}

    language = context.get("language", "csharp")
    module_name = payload.get("module_name", "modul necunoscut")
    criteria = payload.get("acceptance_criteria", [])

    #RAG integration
    relevant_notes = search_vault(module_name)
    context_text = "\n\n".join([f"Nota [{note['vault_note_ref']}]:\n{note['content']}" for note in relevant_notes])

    system_prompt = getPrompt("system", {"language": language})
    # call and implement getUserPrompt to generate the user prompt based on the task and context
    # user_prompt
                       
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    try:
        result = structured_llm.invoke(messages)
    except ValidationError as e:
        raise RuntimeError(f"Validarea AgentResult a eșuat: {e}")
    result = result.model_copy(update={"task_id": task.task_id, "agent_id": "S5"})

    return result

def getPrompt(type: Literal["system", "user"], options: dict) -> str:
    switch = {
        "system": getSystemPrompt,
        "user": getUserPrompt
    }

    
    return switch.get(type, getSystemPrompt(**options))(**options)

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