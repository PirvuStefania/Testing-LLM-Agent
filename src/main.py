from src.contracts import AgentTask
from src.agent_node import run_test_gen_agent

if __name__ == "__main__":
    # Simulam un task complet trimis catre agentul S5
    mock_task = AgentTask(
        task_id="002",
        agent_id="S5",
        task_type="generate_tests",
        input_payload={
            "module_name": "auth",
            "acceptance_criteria": [
                "Given a valid token, the endpoint returns status 200 and user data",
                "Given an invalid or expired token, the endpoint returns status 401"
            ]
        },
        context={
            "description": "Testarea fluxului de securitate și token-uri JWT",
            "language": "csharp"
        }
    )

    print(f"pornire agent S5 cu rag pentru {mock_task.input_payload['module_name']}")
    result = run_test_gen_agent(mock_task)

    print("\n--- REZULTAT VALIDAT DE CONTRACTUL AGENTULUI ---")
    print(f"Status Task: {result.status}")
    print(f"Clasa de Evidență: {result.evidence_class}")
    print(f"Nivel de Încredere: {result.confidence}")
    print(f"Raționament: {result.rationale}")
    
    print("\nLanțul de pași (Reasoning Chain):")
    for step in result.reasoning_chain:
        print(f"  - {step}")

    print("\n--- CODUL PYTEST GENERAT ---")
    print(result.artifacts[0].content)

    print("\n--- AGENT RESULT (JSON FORMAT) ---")
    print(result.model_dump_json(indent=2))