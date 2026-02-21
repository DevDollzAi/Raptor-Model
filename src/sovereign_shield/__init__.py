# Sovereign Shield Implementation v1.0
# Architecture of Sovereign Stability
# Bio-Hash Protocol, BARK Protocol, Inevitability Gate, C=0 Proof Chains

"""
Sovereign Shield - Deterministic Infrastructure Protection System

This module implements the core components of the Sovereign Shield architecture:
- Bio-Hash Protocol: Cryptographic identity anchored to human operators
- BARK Protocol: Identity violation detection and recursive validation
- Inevitability Gate: Five-stage liquidity threshold system
- C=0 Proof Chain: Deterministic verification of operations

Author: Nicholas Michael Grossi - Capability Architect
System: AxiomHive - Deterministic Truth Engine
"""

__version__ = "1.0.0"
__author__ = "Nicholas Michael Grossi"
__locus__ = "Alexis M. Adams - System Architect, AxiomHive Owner, LOP Authority"

from sovereign_shield.core import (
    SovereignShield,
    WealthNode,
    CapitalFlowVector,
    ShieldStatus
)

from sovereign_shield.bio_hash import (
    BioHashGenerator,
    HDIdentitySystem,
    DIDGenerator,
    TrajectoryProcessor
)

from sovereign_shield.bark import (
    BARKValidator,
    IdentityViolationDetector,
    AxiomValidator,
    FixedPointConvergence
)

from sovereign_shield.inevitability_gate import (
    InevitabilityGate,
    GateStage,
    LiquidityThreshold,
    StageExecution,
    GateController
)

from sovereign_shield.proof_chain import (
    ProofChainGenerator,
    C0Verifier,
    ZeroEntropyExecutor,
    DeterministicReceipt
)

from sovereign_shield.config import (
    ShieldConfig,
    BioHashConfig,
    BARKConfig,
    InevitabilityGateConfig,
    ProofChainConfig,
    DEFAULT_CONFIG
)

from sovereign_shield.response_policy import (
    ResponsePolicy,
    OperatorConstraintRegistry,
    SourceCitation,
    PolicyResponse,
    PolicyEvaluation,
    PolicyViolation,
    FactualDomain,
    PolicyGateResult,
    RESPONSE_PREAMBLE,
    ABSTRACTION_MARKER,
)

__all__ = [
    # Core
    "SovereignShield",
    "WealthNode", 
    "CapitalFlowVector",
    "ShieldStatus",
    # Bio-Hash
    "BioHashGenerator",
    "HDIdentitySystem",
    "DIDGenerator",
    "TrajectoryProcessor",
    # BARK
    "BARKValidator",
    "IdentityViolationDetector",
    "AxiomValidator",
    "FixedPointConvergence",
    # Inevitability Gate
    "InevitabilityGate",
    "GateStage",
    "LiquidityThreshold",
    "StageExecution",
    "GateController",
    # Proof Chain
    "ProofChainGenerator",
    "C0Verifier",
    "ZeroEntropyExecutor",
    "DeterministicReceipt",
    # Configuration
    "ShieldConfig",
    "BioHashConfig",
    "BARKConfig",
    "InevitabilityGateConfig",
    "ProofChainConfig",
    "DEFAULT_CONFIG",
    # Response Policy
    "ResponsePolicy",
    "OperatorConstraintRegistry",
    "SourceCitation",
    "PolicyResponse",
    "PolicyEvaluation",
    "PolicyViolation",
    "FactualDomain",
    "PolicyGateResult",
    "RESPONSE_PREAMBLE",
    "ABSTRACTION_MARKER",
]
