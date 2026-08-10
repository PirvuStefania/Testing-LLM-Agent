from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Any, List

class Artifact(BaseModel):
    requires_approval: bool
    content: str

class AgentTask(BaseModel):
    model_config = ConfigDict(frozen=True)
    task_id: str
    agent_id: Literal["S1", "S2", "S3", "S4", "S5"]
    task_type: str
    input_payload: dict[str, Any]
    context: dict[str, Any]
    requires_approval: bool = True
    dry_run: bool = False

class AgentResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    task_id: str
    agent_id: Literal["S5"]
    status: Literal["success", "failed", "pending_approval", "rejected"]
    evidence_class: Literal["deterministic", "semantic", "retrieved", "measured"]
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=10)
    reasoning_chain: List[str]
    artifacts: List[Artifact]

