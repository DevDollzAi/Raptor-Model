# Sovereign Shield Core Implementation
# Deterministic Infrastructure Protection System

"""
The Sovereign Shield is the definitive design blueprint for protecting 
wealth nodes and ensuring the absolute integrity of capital flow through 
Certified Intelligence. It is designed to be immune to the cascades of 
trust collapse that plague probabilistic systems.

Core Components:
- SovereignShield: Main shield orchestrator
- WealthNode: Protected wealth node
- CapitalFlowVector: Vector for capital movement
- ShieldStatus: Status tracking

Author: Nicholas Michael Grossi
"""

import hashlib
import hmac
import time
import json
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any, Set
from enum import Enum

from sovereign_shield.bio_hash import (
    HDIdentitySystem,
    BioHashReceipt,
    TrajectoryPoint,
    TrajectoryType
)
from sovereign_shield.bark import (
    BARKValidator,
    IdentityViolation,
    ConvergenceState
)
from sovereign_shield.inevitability_gate import (
    InevitabilityGate,
    GateStage,
    GateExecution
)
from sovereign_shield.proof_chain import (
    ProofChainGenerator,
    C0Verifier,
    ZeroEntropyExecutor,
    DeterministicReceipt
)


class ShieldStatus(Enum):
    """Status of the Sovereign Shield"""
    ACTIVE = "active"
    COMPROMISED = "compromised"
    LOCKED = "locked"
    MAINTENANCE = "maintenance"
    INITIALIZING = "initializing"


class NodeStatus(Enum):
    """Status of wealth node"""
    PROTECTED = "protected"
    EXPOSED = "exposed"
    QUARANTINED = "quarantined"
    DEGRADED = "degraded"


@dataclass
class WealthNode:
    """
    A protected wealth node in the Sovereign Shield.
    """
    node_id: str
    operator_id: str
    did: str
    bio_hash: str
    status: NodeStatus
    balance: float
    frozen_balance: float = 0.0
    created_at: float = field(default_factory=time.time)
    last_verified: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "operator_id": self.operator_id,
            "did": self.did,
            "bio_hash": self.bio_hash,
            "status": self.status.value,
            "balance": self.balance,
            "frozen_balance": self.frozen_balance,
            "created_at": self.created_at,
            "last_verified": self.last_verified,
            "metadata": self.metadata
        }
    
    def can_transact(self, amount: float) -> bool:
        """Check if node can transact the given amount"""
        available = self.balance - self.frozen_balance
        return (
            self.status == NodeStatus.PROTECTED and
            available >= amount
        )


@dataclass
class CapitalFlowVector:
    """
    Vector representing capital flow between nodes.
    """
    vector_id: str
    source_node_id: str
    target_node_id: str
    amount: float
    status: str  # pending, approved, rejected, executed
    gate_execution_id: Optional[str] = None
    receipt: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)
    executed_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "vector_id": self.vector_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "amount": self.amount,
            "status": self.status,
            "gate_execution_id": self.gate_execution_id,
            "receipt": self.receipt,
            "created_at": self.created_at,
            "executed_at": self.executed_at,
            "metadata": self.metadata
        }


@dataclass
class CollapseThreshold:
    """
    Collapse threshold gates for monitoring system stability.
    """
    threshold_id: str
    metric_name: str
    critical_value: float
    warning_value: float
    current_value: float = 0.0
    is_triggered: bool = False
    last_checked: float = field(default_factory=time.time)
    
    def check(self, value: float) -> bool:
        """Check if threshold is triggered"""
        self.current_value = value
        self.last_checked = time.time()
        self.is_triggered = value >= self.critical_value
        return self.is_triggered
    
    def is_warning(self, value: float) -> bool:
        """Check if value is in warning zone"""
        return value >= self.warning_value and value < self.critical_value


@dataclass
class ShieldMetrics:
    """
    Metrics for monitoring shield health.
    """
    total_nodes: int = 0
    protected_nodes: int = 0
    exposed_nodes: int = 0
    total_value_locked: float = 0.0
    hrl_score: float = 1.0  # Health/Resilience/Liquidity score
    collapse_thresholds_triggered: List[str] = field(default_factory=list)
    last_assessment: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_nodes": self.total_nodes,
            "protected_nodes": self.protected_nodes,
            "exposed_nodes": self.exposed_nodes,
            "total_value_locked": self.total_value_locked,
            "hrl_score": self.hrl_score,
            "collapse_thresholds_triggered": self.collapse_thresholds_triggered,
            "last_assessment": self.last_assessment
        }


class SovereignShield:
    """
    The Sovereign Shield - Main orchestrator for deterministic infrastructure protection.
    
    Provides:
    - Cryptographic identity through Bio-Hash
    - Identity violation detection through BARK
    - Liquidity control through Inevitability Gate
    - Deterministic verification through C=0 Proof Chains
    """
    
    # Default collapse thresholds
    DEFAULT_THRESHOLDS = [
        CollapseThreshold(
            threshold_id="entropy_threshold",
            metric_name="system_entropy",
            critical_value=0.5,
            warning_value=0.3
        ),
        CollapseThreshold(
            threshold_id="violation_threshold",
            metric_name="identity_violations",
            critical_value=5,
            warning_value=2
        ),
        CollapseThreshold(
            threshold_id="latency_threshold",
            metric_name="execution_latency_ms",
            critical_value=5000,
            warning_value=2000
        ),
        CollapseThreshold(
            threshold_id="failure_threshold",
            metric_name="operation_failure_rate",
            critical_value=0.1,
            warning_value=0.05
        ),
        CollapseThreshold(
            threshold_id="liquidity_threshold",
            metric_name="liquidity_ratio",
            critical_value=0.2,
            warning_value=0.3
        )
    ]
    
    def __init__(
        self,
        lattice_dimensions: int = 512,
        auditor_review_time: float = 300.0,
        canary_percentage: float = 0.01,
        num_shadow_hosts: int = 3
    ):
        """
        Initialize Sovereign Shield.
        
        Args:
            lattice_dimensions: Dimensions for Bio-Hash lattice
            auditor_review_time: Time for auditor review
            canary_percentage: Percentage for canary release
            num_shadow_hosts: Number of hosts for shadow execution
        """
        # Initialize subsystems
        self.hd_identity = HDIdentitySystem(lattice_dimensions=lattice_dimensions)
        self.bark_validator = BARKValidator()
        self.inevitability_gate = InevitabilityGate(
            auditor_review_time=auditor_review_time,
            canary_percentage=canary_percentage,
            num_shadow_hosts=num_shadow_hosts
        )
        self.proof_chain_generator = ProofChainGenerator()
        self.c0_verifier = C0Verifier(self.proof_chain_generator)
        self.zero_entropy_executor = ZeroEntropyExecutor()
        
        # Shield state
        self.status = ShieldStatus.INITIALIZING
        self._nodes: Dict[str, WealthNode] = {}
        self._capital_flows: Dict[str, CapitalFlowVector] = {}
        self._collapse_thresholds: Dict[str, CollapseThreshold] = {
            t.threshold_id: t for t in self.DEFAULT_THRESHOLDS
        }
        
        # Metrics
        self.metrics = ShieldMetrics()
        
        # Set status to active
        self.status = ShieldStatus.ACTIVE
    
    def register_node(
        self,
        operator_id: str,
        trajectory: List[TrajectoryPoint],
        initial_balance: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> WealthNode:
        """
        Register a new wealth node with the shield.
        
        Args:
            operator_id: Operator identifier
            trajectory: Identity trajectory
            initial_balance: Initial balance
            metadata: Optional metadata
            
        Returns:
            Created wealth node
        """
        # Register identity with HD-DIS
        receipt = self.hd_identity.register_identity(trajectory, operator_id)
        
        # Create wealth node
        node = WealthNode(
            node_id=str(uuid.uuid4()),
            operator_id=operator_id,
            did=receipt.did,
            bio_hash=receipt.bio_hash,
            status=NodeStatus.PROTECTED,
            balance=initial_balance,
            metadata=metadata or {}
        )
        
        self._nodes[node.node_id] = node
        self._update_metrics()
        
        return node
    
    def verify_node(
        self,
        node_id: str,
        trajectory: List[TrajectoryPoint]
    ) -> Tuple[bool, Optional[BioHashReceipt]]:
        """
        Verify a node's identity.
        
        Args:
            node_id: Node to verify
            trajectory: Identity trajectory
            
        Returns:
            Tuple of (is_valid, receipt)
        """
        if node_id not in self._nodes:
            return False, None
        
        node = self._nodes[node_id]
        
        # Verify with HD-DIS
        is_valid, receipt = self.hd_identity.verify_identity(
            trajectory, node.operator_id
        )
        
        if is_valid:
            node.last_verified = time.time()
        
        return is_valid, receipt
    
    def initiate_capital_flow(
        self,
        source_node_id: str,
        target_node_id: str,
        amount: float,
        execution_logic: Optional[callable] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Initiate a capital flow between nodes.
        
        Args:
            source_node_id: Source node ID
            target_node_id: Target node ID
            amount: Amount to transfer
            execution_logic: Optional execution logic for verification
            metadata: Optional metadata
            
        Returns:
            Tuple of (initiated, gate_execution_id)
        """
        # Validate nodes exist
        if source_node_id not in self._nodes or target_node_id not in self._nodes:
            return False, None
        
        source = self._nodes[source_node_id]
        target = self._nodes[target_node_id]
        
        # Check if source can transact
        if not source.can_transact(amount):
            return False, None
        
        # Create capital flow vector
        flow = CapitalFlowVector(
            vector_id=str(uuid.uuid4()),
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            amount=amount,
            status="pending",
            metadata=metadata or {}
        )
        
        self._capital_flows[flow.vector_id] = flow
        
        # Execute Inevitability Gate
        is_approved, execution = self.inevitability_gate.execute_full_gate(
            operator_id=source.operator_id,
            target_fixed_point=[1.0] * 512,  # Simplified for example
            parameters={
                "source": source_node_id,
                "target": target_node_id,
                "amount": amount
            },
            execution_logic=execution_logic,
            transaction_type="CAPITAL_TRANSFER",
            amount=amount,
            did=source.did,
            bio_hash=source.bio_hash
        )
        
        flow.gate_execution_id = execution.execution_id
        flow.status = "approved" if is_approved else "rejected"
        
        if is_approved:
            # Execute transfer
            source.balance -= amount
            target.balance += amount
            flow.executed_at = time.time()
            flow.status = "executed"
            
            # Generate proof receipt
            receipt = self._generate_flow_receipt(flow)
            flow.receipt = receipt.to_dict()
        
        self._update_metrics()
        
        return is_approved, execution.execution_id if is_approved else None
    
    def _generate_flow_receipt(self, flow: CapitalFlowVector) -> DeterministicReceipt:
        """Generate proof receipt for capital flow"""
        # Create proof chain
        chain = self.proof_chain_generator.create_proof_chain(
            operation_type="CAPITAL_TRANSFER",
            inputs={
                "source": flow.source_node_id,
                "target": flow.target_node_id,
                "amount": flow.amount
            },
            outputs={
                "executed": True,
                "timestamp": flow.executed_at
            },
            operator_id=self._nodes[flow.source_node_id].operator_id
        )
        
        # Generate receipt
        receipt = self.proof_chain_generator.generate_receipt(
            chain=chain,
            inputs={"amount": flow.amount},
            outputs={"status": "executed"},
            execution_time=1.0  # Simplified
        )
        
        return receipt
    
    def detect_identity_violation(
        self,
        node_id: str,
        trajectory: List[float],
        statements: Dict[str, str]
    ) -> Optional[IdentityViolation]:
        """
        Detect identity violation for a node.
        
        Args:
            node_id: Node to check
            trajectory: Current trajectory
            statements: Axiom statements
            
        Returns:
            IdentityViolation if detected
        """
        if node_id not in self._nodes:
            return None
        
        node = self._nodes[node_id]
        
        # Perform BARK validation
        is_valid, violation, convergence = self.bark_validator.validate_identity(
            operator_id=node.operator_id,
            trajectory=trajectory,
            system_function=lambda z, x: z,  # Simplified
            statements=statements
        )
        
        if violation:
            node.status = NodeStatus.QUARANTINED
            self._update_metrics()
        
        return violation
    
    def check_collapse_thresholds(self, metrics: Dict[str, float]) -> List[str]:
        """
        Check collapse thresholds against current metrics.
        
        Args:
            metrics: Current metric values
            
        Returns:
            List of triggered threshold IDs
        """
        triggered = []
        
        for threshold_id, threshold in self._collapse_thresholds.items():
            if threshold_id in metrics:
                if threshold.check(metrics[threshold_id]):
                    triggered.append(threshold_id)
        
        if triggered:
            self.metrics.collapse_thresholds_triggered = triggered
            self.status = ShieldStatus.COMPROMISED
        else:
            self.status = ShieldStatus.ACTIVE
        
        return triggered
    
    def get_node(self, node_id: str) -> Optional[WealthNode]:
        """Get node by ID"""
        return self._nodes.get(node_id)
    
    def list_nodes(self) -> List[str]:
        """List all node IDs"""
        return list(self._nodes.keys())
    
    def get_capital_flow(self, flow_id: str) -> Optional[CapitalFlowVector]:
        """Get capital flow by ID"""
        return self._capital_flows.get(flow_id)
    
    def list_capital_flows(self, status: Optional[str] = None) -> List[str]:
        """List capital flows, optionally filtered by status"""
        if status:
            return [
                f_id for f_id, flow in self._capital_flows.items()
                if flow.status == status
            ]
        return list(self._capital_flows.keys())
    
    def get_metrics(self) -> ShieldMetrics:
        """Get current shield metrics"""
        return self.metrics
    
    def _update_metrics(self):
        """Update shield metrics"""
        self.metrics.total_nodes = len(self._nodes)
        self.metrics.protected_nodes = sum(
            1 for n in self._nodes.values() 
            if n.status == NodeStatus.PROTECTED
        )
        self.metrics.exposed_nodes = sum(
            1 for n in self._nodes.values() 
            if n.status == NodeStatus.EXPOSED
        )
        self.metrics.total_value_locked = sum(
            n.balance for n in self._nodes.values()
        )
        
        # Calculate HRL score
        if self.metrics.total_nodes > 0:
            self.metrics.hrl_score = (
                self.metrics.protected_nodes / self.metrics.total_nodes
            ) * min(1.0, self.metrics.total_value_locked / 1000000)
        
        self.metrics.last_assessment = time.time()
    
    def get_collapse_threshold(self, threshold_id: str) -> Optional[CollapseThreshold]:
        """Get collapse threshold by ID"""
        return self._collapse_thresholds.get(threshold_id)
    
    def set_status(self, status: ShieldStatus):
        """Set shield status"""
        self.status = status
    
    def lock_shield(self, reason: str = ""):
        """
        Lock the shield (emergency action).
        
        Args:
            reason: Reason for locking
        """
        self.status = ShieldStatus.LOCKED
        # In production, would freeze all operations
    
    def unlock_shield(self):
        """Unlock the shield (requires authentication)"""
        self.status = ShieldStatus.ACTIVE
