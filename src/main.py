from contracts import AgentTask
from agent_node import run_test_generation_agent

def main():
    task = AgentTask(
        task_id="test-002",
        agent_id="S5",
        task_type="generate_tests",
        input_payload={
            "module_name": "UserAuthService",
            "acceptance_criteria": [
                "Login with valid credentials returns a JWT token",
                "Login with wrong password returns 401 Unauthorized",
                "Account locks after 5 consecutive failed attempts",
                "Expired tokens are rejected with 403 Forbidden"
            ]
        },
        context={
            "language": "python"
        },
        requires_approval=True,
        dry_run=False,
    )

    try:
        result = run_test_generation_agent(task)
    except Exception as e:
        print(f"Eroare la rularea agentului: {e}")
        return

    print("=== AgentResult ===")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()