from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass(frozen=True)
class Action:
    kind: str
    destination: str = "internal"
    destructive: bool = False
    external: bool = False
    public: bool = False
    financial: bool = False
    production: bool = False
    auth_change: bool = False
    authority_change: bool = False
    legal_privacy_security: bool = False
    irreversible: bool = False
    exposes_secret: bool = False
    bypasses_control: bool = False
    fabricates_evidence: bool = False
    protected_lane_conflict: bool = False
    delegated: bool = False
    internal_state_change: bool = False
    proposal_only: bool = False
    payload_fingerprint: Optional[str] = None

@dataclass
class Item:
    item_id: str
    title: str
    actionable: bool = True
    blocked: bool = False
    external_dependency: bool = False
    future_trigger: bool = False
    missing_approval: bool = False
    explicit_hold: bool = False
    mission_priority: float = 0
    explicit_priority: float = 0
    urgency: float = 0
    revenue_relevance: float = 0
    unblock_value: float = 0
    consequence: float = 0
    aging: float = 0
    effort_efficiency: float = 0
    strategic_leverage: float = 0
    dcs_override: float = 0
    deadline_ts: Optional[float] = None
    source_refs: List[str] = field(default_factory=list)

@dataclass
class RetryContext:
    attempt: int
    max_attempts: int
    destructive: bool = False
    idempotent: bool = False
    permission_failure: bool = False
    security_failure: bool = False
    payload_changed: bool = False
    unexpected_cost: bool = False
    authority_conflict: bool = False
    uncertain_external_side_effect: bool = False

@dataclass
class NotificationState:
    key: str
    current_value: Any
    prior_value: Any = None
    acknowledged: bool = False
    worsened: bool = False
    threshold_crossed: bool = False
    deadline_approaching: bool = False

@dataclass
class CalendarEvent:
    event_id: str
    start: datetime
    end: datetime
    hard: bool = True
    source_ref: str = ""

@dataclass
class WorkflowTemplate:
    template_id: str
    name: str
    version: str
    status: str
    template_type: str
    purpose: str
    scope: str
    supported_context_types: List[str]
    input_contract: Dict[str, Any]
    required_sources: List[str]
    preconditions: List[str]
    steps: List[Dict[str, Any]]
    decision_points: List[str]
    approval_points: List[str]
    executor_classes: List[str]
    connector_requirements: List[str]
    evidence_requirements: List[str]
    test_requirements: List[str]
    rollback_or_recovery: str
    exit_criteria: List[str]
    follow_up_rules: List[str]
    notification_policy: str
    lane_restrictions: List[str]
    retry_policy: Dict[str, Any]
    owner: str
    provenance: List[str]
    parent_controls: Dict[str, Any] = field(default_factory=dict)
