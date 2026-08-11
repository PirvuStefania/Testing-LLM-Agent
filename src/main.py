from src.contracts import AgentTask
from src.agent_node import run_test_gen_agent

def main():
    task = AgentTask(
        task_id="test-001",
        agent_id="S5",
        task_type="generate_tests",
        input_payload={
            "module_name": "Calculator",
            "acceptance_criteria": [
                "Adunarea a doua numere returneaza suma corecta",
                "Impartirea la zero arunca o exceptie"
            ]
        },
        context={
            "language": "csharp"
        },
        requires_approval=True,
        dry_run=False
    )

    try:
        result = run_test_gen_agent(task)
    except Exception as e:
        print(f"Eroare la rularea agentului: {e}")
        return

    print("=== AgentResult ===")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()