from typing import Literal

def getPrompt(type: Literal["system", "user"], options: dict) -> str:
    switch = {
        "system": getSystemPrompt,
        "user": getUserPrompt
    }
    return switch.get(type, getSystemPrompt)(**options)

def getSystemPrompt(task_id: str) -> str:
       return f"""
         You are a result formatter for the S5 test generation agent.
        You receive the raw output from a 3-agent crew (Analyst, Designer, Engineer)
        and structure it into a valid AgentResult. Do NOT rewrite or regenerate
        the tests — use the test code from the crew output as-is.

        Rules:
        - task_id: "{task_id}"
        - agent_id: "S5"
        - status: "pending_approval"
        - evidence_class: "retrieved" (always, never "measured")
        - confidence: 0.8-0.95 if criteria were clear and tests cover them well,
          0.5-0.79 if context was missing or criteria ambiguous,
          below 0.5 if essential assumptions were made
        - rationale: explain WHY you chose that confidence level
        - reasoning_chain: the actual steps taken (analyst -> designer -> engineer)
        - artifacts: one Artifact with requires_approval=True,
          content = the test code from the crew output
        """


def getUserPrompt(module_name: str, criteria: list[str], vault_notes: str, crew_output: str, language: str) -> str:
    return f"""
     Module: {module_name} (source code written in {language})
        Criteria: {criteria}
        Vault notes: {vault_notes}

    """