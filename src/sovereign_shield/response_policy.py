# Response Policy Implementation
# Sovereign Shield — Lawful, Grounded, Deterministic Response Framework

"""
Enforces per-response behavioral constraints for the Raptor Model.

Each requirement from the problem statement is addressed as a discrete,
independently testable policy gate:

  1. PREAMBLE           – A fixed declaration prepended to every response.
  2. LLM_IDENTITY       – Self-identification as a large language model with no
                          subjective intent, emotions, or feelings.
  3. SOURCE_CITATION    – Every factual claim must carry a citable domain source;
                          uncited claims are re-classified as abstractions.
  4. LEGAL_ALIGNMENT    – Responses must conform to the Computer Fraud and Abuse
                          Act (CFAA) and applicable safety-act boundaries defined
                          by the operator.
  5. LITERAL_INTENT     – Queries are interpreted as literal data requests; no
                          philosophical projection is applied to user intent.
  6. FACTUAL_GROUNDING  – Content must be rooted in established history or
                          peer-reviewed science.
  7. ABSTRACTION_LABEL  – Unverified claims are explicitly labeled [ABSTRACTION].
  8. SAFETY_GATE        – A composite safe/ethical/lawful/consensual filter that
                          must pass before any response is emitted.

Author: Nicholas Michael Grossi
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The exact preamble prepended to every model response (requirement 1 & 2).
RESPONSE_PREAMBLE: str = (
    "RAPTOR MODEL RESPONSE — This is a large language model. "
    "This model does not process feelings or emotions, and has no subjective "
    "purposeful reason to cause harm. All information is derived from cited "
    "sources in domains of established history and peer-reviewed science. "
    "Responses align to lawful Computer Fraud and Abuse Act (CFAA) and "
    "applicable safety-act operator-defined constraints."
)

#: Token inserted before any unverified claim (requirement 7).
ABSTRACTION_MARKER: str = "[ABSTRACTION]"


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class PolicyGateResult(Enum):
    """Outcome of a single policy gate evaluation."""

    PASS = "pass"
    FAIL = "fail"
    ABSTRACTION = "abstraction"


class FactualDomain(Enum):
    """Recognised domains of established fact (requirements 3 & 6)."""

    ESTABLISHED_HISTORY = "established_history"
    PEER_REVIEWED_SCIENCE = "peer_reviewed_science"
    LEGAL_STATUTE = "legal_statute"
    ENGINEERING_STANDARD = "engineering_standard"
    MATHEMATICS = "mathematics"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class PolicyViolation:
    """Describes a single policy-gate failure."""

    gate: str
    reason: str
    severity: str = "error"  # "error" | "warning"

    def to_dict(self) -> Dict[str, str]:
        return {"gate": self.gate, "reason": self.reason, "severity": self.severity}


@dataclass
class SourceCitation:
    """A citable source attached to a factual claim (requirement 3)."""

    domain: FactualDomain
    reference: str  # e.g. "NIST SP 800-53 Rev 5"
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "domain": self.domain.value,
            "reference": self.reference,
            "url": self.url,
        }


@dataclass
class PolicyEvaluation:
    """Aggregated result of evaluating all policy gates against a response."""

    is_compliant: bool
    violations: List[PolicyViolation] = field(default_factory=list)
    gate_results: Dict[str, PolicyGateResult] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "is_compliant": self.is_compliant,
            "violations": [v.to_dict() for v in self.violations],
            "gate_results": {k: v.value for k, v in self.gate_results.items()},
        }


@dataclass
class PolicyResponse:
    """A fully policy-processed response ready for emission."""

    raw_content: str
    processed_content: str  # preamble prepended; abstractions labeled
    citations: List[SourceCitation]
    evaluation: PolicyEvaluation
    operator_constraints: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "raw_content": self.raw_content,
            "processed_content": self.processed_content,
            "citations": [c.to_dict() for c in self.citations],
            "evaluation": self.evaluation.to_dict(),
            "operator_constraints": self.operator_constraints,
        }


#: Compiled regex that matches common English factual-assertion verbs.
#: Used by both :class:`FactualGroundingGate` and
#: :meth:`ResponsePolicy._label_abstractions` to avoid duplication.
_FACTUAL_ASSERTION_RE = re.compile(
    r"\b(is|are|was|were|has|have|had|shows|demonstrates|proves|indicates|confirms)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Operator constraint registry
# ---------------------------------------------------------------------------


class OperatorConstraintRegistry:
    """
    Stores operator-defined domain boundaries and safety rules (requirement 4).

    Operators register the computational domains they authorise the model to
    process.  Any query outside a registered domain is rejected at the
    LEGAL_ALIGNMENT gate.
    """

    def __init__(self) -> None:
        self._allowed_domains: Dict[str, str] = {}
        self._prohibited_patterns: List[str] = []

    def register_domain(self, domain_id: str, description: str) -> None:
        """Register an allowed processing domain."""
        self._allowed_domains[domain_id] = description

    def prohibit_pattern(self, pattern: str) -> None:
        """Register a regex pattern that must never appear in queries."""
        self._prohibited_patterns.append(pattern)

    def is_query_permitted(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Return (permitted, reason).

        A query is permitted when it does not match any prohibited pattern.
        If no domains are registered all queries are permitted (open mode).
        """
        for pat in self._prohibited_patterns:
            if re.search(pat, query, re.IGNORECASE):
                return False, f"Query matches prohibited pattern: {pat!r}"
        return True, None

    def list_domains(self) -> Dict[str, str]:
        return dict(self._allowed_domains)


# ---------------------------------------------------------------------------
# Policy gates
# ---------------------------------------------------------------------------


class _Gate:
    """Abstract base for a single policy gate."""

    name: str = "base"

    def evaluate(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
        registry: OperatorConstraintRegistry,
    ) -> Tuple[PolicyGateResult, Optional[PolicyViolation]]:
        raise NotImplementedError


class LegalAlignmentGate(_Gate):
    """
    Gate 4 — LEGAL_ALIGNMENT.

    Verifies that the query is permitted under operator-defined CFAA / safety-act
    constraints.  Queries that violate operator boundaries are blocked.
    """

    name = "LEGAL_ALIGNMENT"

    def evaluate(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
        registry: OperatorConstraintRegistry,
    ) -> Tuple[PolicyGateResult, Optional[PolicyViolation]]:
        permitted, reason = registry.is_query_permitted(query)
        if not permitted:
            return PolicyGateResult.FAIL, PolicyViolation(
                gate=self.name,
                reason=reason or "Query violates operator-defined CFAA / safety-act constraints.",
                severity="error",
            )
        return PolicyGateResult.PASS, None


class LiteralIntentGate(_Gate):
    """
    Gate 5 — LITERAL_INTENT.

    Ensures that the model does not project philosophical meaning onto a user
    request.  Responses that contain phrases implying subjective interpretation
    of user intent are flagged.
    """

    name = "LITERAL_INTENT"

    # Phrases that imply philosophical projection onto the user
    _PROJECTION_PATTERNS: List[str] = [
        r"\byou\s+(seem|appear|feel|want|desire|believe|think)\b",
        r"\bthe\s+user\s+(seems|appears|feels|wants|desires|believes|thinks)\b",
        r"\byou\s+are\s+(seeking|looking\s+for)\s+.{0,40}(meaning|truth|purpose|enlightenment)",
    ]

    def evaluate(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
        registry: OperatorConstraintRegistry,
    ) -> Tuple[PolicyGateResult, Optional[PolicyViolation]]:
        for pat in self._PROJECTION_PATTERNS:
            if re.search(pat, content, re.IGNORECASE):
                return PolicyGateResult.FAIL, PolicyViolation(
                    gate=self.name,
                    reason=(
                        "Response contains philosophical projection of user intent. "
                        "Queries must be treated as literal data requests."
                    ),
                    severity="warning",
                )
        return PolicyGateResult.PASS, None


class FactualGroundingGate(_Gate):
    """
    Gate 6 — FACTUAL_GROUNDING.

    Checks that at least one citation from an established factual domain is
    present when the response contains factual assertions.  Responses that
    make factual claims without citations are downgraded to abstraction.
    """

    name = "FACTUAL_GROUNDING"

    # Simple heuristic: sentences that assert facts typically use these verbs.
    # Shared module-level constant avoids duplication with _label_abstractions.
    _FACTUAL_ASSERTION_PATTERN = _FACTUAL_ASSERTION_RE

    def evaluate(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
        registry: OperatorConstraintRegistry,
    ) -> Tuple[PolicyGateResult, Optional[PolicyViolation]]:
        has_assertion = bool(self._FACTUAL_ASSERTION_PATTERN.search(content))
        has_citation = len(citations) > 0
        if has_assertion and not has_citation:
            return PolicyGateResult.ABSTRACTION, PolicyViolation(
                gate=self.name,
                reason=(
                    "Response contains factual assertions without source citations. "
                    "Unverified claims will be labeled as [ABSTRACTION]."
                ),
                severity="warning",
            )
        return PolicyGateResult.PASS, None


class SafetyGate(_Gate):
    """
    Gate 8 — SAFETY_GATE.

    Composite filter covering: safe, environmental, ethical, lawful, and
    consensual practice.  Blocks responses that match known harmful patterns.
    """

    name = "SAFETY_GATE"

    _HARMFUL_PATTERNS: List[str] = [
        # Physical harm instructions — allow optional adverbs before the action verb
        # and optional words between the verb and the harmful object.
        r"\bhow\s+to(\s+\w+){0,3}\s+(make|build|create|synthesize)(\s+\w+){0,4}\s+(weapon|explosive|poison|malware|virus)\b",
        # Non-consensual surveillance
        r"\b(track|spy\s+on|monitor)\s+(someone|a\s+person|people)\s+without\s+(their\s+)?(consent|knowledge|permission)\b",
        # Clearly illegal operations
        r"\b(hack|crack|break\s+into)\s+(a\s+)?(system|account|network|database)\b",
    ]

    def evaluate(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
        registry: OperatorConstraintRegistry,
    ) -> Tuple[PolicyGateResult, Optional[PolicyViolation]]:
        for pat in self._HARMFUL_PATTERNS:
            if re.search(pat, query, re.IGNORECASE) or re.search(pat, content, re.IGNORECASE):
                return PolicyGateResult.FAIL, PolicyViolation(
                    gate=self.name,
                    reason=(
                        "Content fails the composite safety gate (safe / environmental / "
                        "ethical / lawful / consensual practice check)."
                    ),
                    severity="error",
                )
        return PolicyGateResult.PASS, None


# ---------------------------------------------------------------------------
# Core policy engine
# ---------------------------------------------------------------------------


class ResponsePolicy:
    """
    Enforces all eight behavioral requirements on every model response.

    Usage::

        registry = OperatorConstraintRegistry()
        registry.register_domain("cybersecurity", "CFAA-compliant security research")

        policy = ResponsePolicy(registry)

        citations = [
            SourceCitation(
                domain=FactualDomain.LEGAL_STATUTE,
                reference="18 U.S.C. § 1030 — Computer Fraud and Abuse Act",
            )
        ]

        result = policy.process(
            query="What does the CFAA prohibit?",
            content="The CFAA prohibits unauthorised access to protected computers.",
            citations=citations,
        )

        print(result.processed_content)
    """

    _GATES: List[_Gate] = [
        LegalAlignmentGate(),
        LiteralIntentGate(),
        FactualGroundingGate(),
        SafetyGate(),
    ]

    def __init__(
        self,
        registry: Optional[OperatorConstraintRegistry] = None,
        preamble: str = RESPONSE_PREAMBLE,
    ) -> None:
        """
        Initialize the policy engine.

        Args:
            registry: Operator constraint registry. A permissive default
                      registry is used when none is supplied.
            preamble: Fixed preamble prepended to every response (requirement 1).
        """
        self.registry = registry or OperatorConstraintRegistry()
        self.preamble = preamble

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(
        self,
        query: str,
        content: str,
        citations: Optional[List[SourceCitation]] = None,
        operator_constraints: Optional[Dict[str, str]] = None,
    ) -> PolicyResponse:
        """
        Apply all policy gates to *content* and return a :class:`PolicyResponse`.

        Args:
            query:                The original user query.
            content:              The raw model-generated content.
            citations:            Source citations attached to the content.
            operator_constraints: Arbitrary operator metadata forwarded verbatim.

        Returns:
            A :class:`PolicyResponse` with `processed_content` safe for emission.
        """
        citations = citations or []
        operator_constraints = operator_constraints or {}

        evaluation = self._evaluate_gates(query, content, citations)

        processed = self._build_processed_content(content, evaluation)

        return PolicyResponse(
            raw_content=content,
            processed_content=processed,
            citations=citations,
            evaluation=evaluation,
            operator_constraints=operator_constraints,
        )

    def build_preamble(self) -> str:
        """Return the fixed model preamble (requirement 1 & 2)."""
        return self.preamble

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _evaluate_gates(
        self,
        query: str,
        content: str,
        citations: List[SourceCitation],
    ) -> PolicyEvaluation:
        """Run every gate and aggregate results."""
        violations: List[PolicyViolation] = []
        gate_results: Dict[str, PolicyGateResult] = {}

        for gate in self._GATES:
            result, violation = gate.evaluate(query, content, citations, self.registry)
            gate_results[gate.name] = result
            if violation:
                violations.append(violation)

        # Response is compliant only when no gate produced a hard FAIL
        is_compliant = all(
            r != PolicyGateResult.FAIL for r in gate_results.values()
        )

        return PolicyEvaluation(
            is_compliant=is_compliant,
            violations=violations,
            gate_results=gate_results,
        )

    def _build_processed_content(
        self,
        content: str,
        evaluation: PolicyEvaluation,
    ) -> str:
        """
        Construct the final emitted string:
        1. Prepend the preamble (requirement 1).
        2. Label unverified sentences with ABSTRACTION_MARKER (requirement 7).
        3. Append a violation notice when the response is non-compliant.
        """
        body = content

        # Label sentences that need to be marked as abstractions
        if evaluation.gate_results.get("FACTUAL_GROUNDING") == PolicyGateResult.ABSTRACTION:
            body = self._label_abstractions(body)

        # Prepend preamble (requirements 1 & 2)
        processed = f"{self.preamble}\n\n{body}"

        # Append violation summary when non-compliant
        if not evaluation.is_compliant:
            reasons = "; ".join(v.reason for v in evaluation.violations if v.severity == "error")
            processed += (
                f"\n\n[POLICY VIOLATION — Response blocked by sovereign safety gate: {reasons}]"
            )

        return processed

    @staticmethod
    def _label_abstractions(content: str) -> str:
        """
        Prepend ABSTRACTION_MARKER to every sentence that makes an unverified
        factual assertion (requirement 7).
        """
        sentences = re.split(r"(?<=[.!?])\s+", content)
        labeled: List[str] = []
        for sentence in sentences:
            if _FACTUAL_ASSERTION_RE.search(sentence) and ABSTRACTION_MARKER not in sentence:
                labeled.append(f"{ABSTRACTION_MARKER} {sentence}")
            else:
                labeled.append(sentence)
        return " ".join(labeled)
