#!/usr/bin/env python
from pathlib import Path
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from s5_ai_flow.crews.content_crew.content_crew import kickoff_content_crew


class S5FlowState(BaseModel):
    module_name: str = ""
    criteria: str = ""
    vault_notes: str = ""
    test_code: str = ""


class S5Flow(Flow[S5FlowState]):

    @start()
    def plan_content(self, crewai_trigger_payload: dict | None = None):
        print("Planning content")

        if crewai_trigger_payload:
            self.state.module_name = crewai_trigger_payload.get("module_name", "Calculator")
            self.state.criteria = str(crewai_trigger_payload.get("acceptance_criteria", []))
            self.state.vault_notes = crewai_trigger_payload.get("vault_notes", "No vault notes available yet.")
        else:
            self.state.module_name = "Calculator"
            self.state.criteria = "['Adding two numbers returns the correct sum', 'Division by zero throws an exception']"
            self.state.vault_notes = "No vault notes available yet."

        print(f"Module: {self.state.module_name}")
        print(f"Criteria: {self.state.criteria}")

    @listen(plan_content)
    def run_test_generation(self):
        result = kickoff_content_crew(inputs={
            "module_name": self.state.module_name,
            "criteria": self.state.criteria,
            "vault_notes": self.state.vault_notes
        })
        self.state.test_code = result.raw
        print("test generation crew finished.")

    @listen(run_test_generation)
    def save_content(self):
        print("Saving generated tests")
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / "generated_tests.py", "w") as f:
            f.write(self.state.test_code)
        print("Tests saved to output/generated_tests.py")


def kickoff():
    flow = S5Flow()
    flow.kickoff()


if __name__ == "__main__":
    kickoff()
