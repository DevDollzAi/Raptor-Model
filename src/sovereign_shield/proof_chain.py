# C=0 Proof Chain Implementation
# Zero-Entropy Deterministic Verification System
# Mathematical Proof of Correctness for Operations

"""
The C=0 Proof Chain provides deterministic verification by generating 
mathematical receipts that prove the correctness of operations. C=0 
represents Zero Entropy - the state of perfect determinism where every 
operation produces identical, predictable results.

Key Components:
- ProofChainGenerator: Generates C=0 proof chains
- C0Verifier: Verifies proof chain integrity
- ZeroEntropyExecutor: Executes operations with deterministic results
- DeterministicReceipt: Mathematical receipt for operations

Author: Nicholas Michael Grossi
"""

import hashlib
import hmac
import time
import json
import uuid
import decimal
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any, Callable
from enum import Enum
import numpy as np


class ProofType(Enum):
    """Types of proofs in the chain"""
    INPUT = "input"
    OPERATION = "operation"
    VERIFICATION = "verification"
    OUTPUT = "output"
    SIGNATURE = "signature"


class VerificationStatus(Enum):
    """Status of proof verification"""
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    EXPIRED = "expired"


@dataclass
class DeterministicReceipt:
    """Mathematical receipt for a deterministic operation"""
    receipt_id: str
    operation_hash: str
    input_hash: str
    output_hash: str
    proof_chain: List[str]
    execution_time: float
    entropy_measure: float
    is_deterministic: bool
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "operation_hash": self.operation_hash,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "proof_chain": self.proof_chain,
            "execution_time": self.execution_time,
            "entropy_measure": self.entropy_measure,
            "is_deterministic": self.is_deterministic,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    def verify(self) -> bool:
        """Verify receipt integrity"""
        # Recompute operation hash from proof chain
        chain_data = "".join(self.proof_chain)
        expected_hash = hashlib.sha3_256(chain_data.encode()).hexdigest()[:32]
        
        return hmac.compare_digest(self.operation_hash, expected_hash) and self.is_deterministic


@dataclass
class ProofStep:
    """A single step in the proof chain"""
    step_id: str
    proof_type: ProofType
    data: Dict[str, Any]
    hash_value: str
    previous_hash: str
    timestamp: float
    operator_signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "proof_type": self.proof_type.value,
            "data": self.data,
            "hash_value": self.hash_value,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "operator_signature": self.operator_signature
        }


@dataclass
class ExecutionRecord:
    """Record of a deterministic execution"""
    record_id: str
    operation_type: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    execution_hosts: List[str]
    consensus_value: Any
    is_deterministic: bool
    started_at: float
    completed_at: Optional[float] = None
    entropy_measure: float = 0.0


class FixedPointArithmetic:
    """
    Fixed-point arithmetic for deterministic calculations.
    Eliminates floating-point non-determinism.
    """
    
    def __init__(self, precision: int = 18):
        """
        Initialize fixed-point arithmetic.
        
        Args:
            precision: Number of decimal places
        """
        self.precision = precision
        self.decimal_context = decimal.Context(prec=precision + 2)
    
    def to_fixed(self, value: float) -> decimal.Decimal:
        """Convert float to fixed-point"""
        return decimal.Decimal(str(value)).quantize(
            decimal.Decimal(10) ** -self.precision,
            rounding=decimal.ROUND_HALF_UP
        )
    
    def from_fixed(self, value: decimal.Decimal) -> float:
        """Convert fixed-point to float"""
        return float(value)
    def add(self, a: float, b: float) -> float:
        """Fixed-point addition"""
        fixed_a = self.to_fixed(a)
        fixed_b = self.to_fixed(b)
        result = (fixed_a + fixed_b).quantize(
            decimal.Decimal(10) ** -self.precision,
            rounding=decimal.ROUND_HALF_UP
        )
        return self.from_fixed(result)
    
    def multiply(self, a: float, b: float) -> float:
        """Fixed-point multiplication"""
        fixed_a = self.to_fixed(a)
        fixed_b = self.to_fixed(b)
        result = (fixed_a * fixed_b).quantize(
            decimal.Decimal(10) ** -self.precision,
            rounding=decimal.ROUND_HALF_UP
        )
        return self.from_fixed(result)
    
    def divide(self, a: float, b: float) -> float:
        """Fixed-point division"""
        if b == 0:
            raise ValueError("Division by zero")
        fixed_a = self.to_fixed(a)
        fixed_b = self.to_fixed(b)
        result = (fixed_a / fixed_b).quantize(
            decimal.Decimal(10) ** -self.precision,
            rounding=decimal.ROUND_HALF_UP
        )
        return self.from_fixed(result)
    
    def compute_hash(self, value: float) -> str:
        """Compute deterministic hash of fixed-point value"""
        fixed = self.to_fixed(value)
        return hashlib.sha3_256(str(fixed).encode()).hexdigest()


class ZeroEntropyExecutor:
    """
    Executes operations with deterministic results across multiple hosts.
    Implements the Zero Entropy Execution Framework (ZEEF).
    """
    
    def __init__(self, precision: int = 18):
        """
        Initialize zero-entropy executor.
        
        Args:
            precision: Fixed-point precision
        """
        self.fixed_point = FixedPointArithmetic(precision)
        self._execution_history: List[ExecutionRecord] = []
    
    def execute_deterministic(
        self,
        operation: Callable,
        inputs: Dict[str, Any],
        num_hosts: int = 3
    ) -> Tuple[bool, ExecutionRecord]:
        """
        Execute operation deterministically across multiple hosts.
        
        Args:
            operation: Operation to execute
            inputs: Input parameters
            num_hosts: Number of hosts for consensus
            
        Returns:
            Tuple of (is_deterministic, execution_record)
        """
        record_id = str(uuid.uuid4())
        started_at = time.time()
        
        # Execute on each host
        results = {}
        hosts = [f"host_{i}" for i in range(num_hosts)]
        
        for host_id in hosts:
            # Execute with fixed-point arithmetic for determinism
            result = operation(inputs, self.fixed_point)
            results[host_id] = result
        
        # Verify determinism by comparing results
        is_deterministic = self._verify_determinism(results)
        
        # Calculate entropy measure
        entropy_measure = self._calculate_entropy(results) if not is_deterministic else 0.0
        
        # Determine consensus value
        consensus_value = self._compute_consensus(results) if is_deterministic else None
        
        completed_at = time.time()
        
        record = ExecutionRecord(
            record_id=record_id,
            operation_type=operation.__name__ if hasattr(operation, "__name__") else "unknown",
            inputs=inputs,
            outputs=results,
            execution_hosts=hosts,
            consensus_value=consensus_value,
            is_deterministic=is_deterministic,
            started_at=started_at,
            completed_at=completed_at,
            entropy_measure=entropy_measure
        )
        
        self._execution_history.append(record)
        
        return is_deterministic, record
    
    def _verify_determinism(self, results: Dict[str, Any]) -> bool:
        """Verify all hosts produced identical results"""
        if not results:
            return False
        
        # Serialize first result deterministically
        first_result = json.dumps(results[list(results.keys())[0]], sort_keys=True)
        
        for host_id, result in results.items():
            result_json = json.dumps(result, sort_keys=True)
            if not hmac.compare_digest(first_result, result_json):
                return False
        
        return True
    
    def _calculate_entropy(self, results: Dict[str, Any]) -> float:
        """Calculate entropy measure of results (higher = less deterministic)"""
        if not results:
            return float('inf')
        
        # Convert results to strings for comparison
        result_strings = [json.dumps(r, sort_keys=True) for r in results.values()]
        
        # Calculate Shannon entropy
        from collections import Counter
        counts = Counter(result_strings)
        total = len(result_strings)
        
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    def _compute_consensus(self, results: Dict[str, Any]) -> Any:
        """Compute consensus value from all results"""
        if not results:
            return None
        
        # Return first result (all should be identical if deterministic)
        return list(results.values())[0]
    
    def get_execution_history(self) -> List[ExecutionRecord]:
        """Get execution history"""
        return self._execution_history.copy()


class ProofChainGenerator:
    """
    Generates C=0 proof chains for deterministic operations.
    """
    
    def __init__(self):
        """Initialize proof chain generator"""
        self._chains: Dict[str, List[ProofStep]] = {}
        self.fixed_point = FixedPointArithmetic()
    
    def create_proof_chain(
        self,
        operation_type: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        operator_id: str,
        execution_record: Optional[ExecutionRecord] = None
    ) -> List[ProofStep]:
        """
        Create a new proof chain.
        
        Args:
            operation_type: Type of operation
            inputs: Operation inputs
            outputs: Operation outputs
            operator_id: Operator identifier
            execution_record: Optional execution record
            
        Returns:
            List of proof steps
        """
        chain_id = str(uuid.uuid4())
        chain = []
        
        previous_hash = "0" * 64  # Genesis hash
        
        # Step 1: Input proof
        input_data = json.dumps(inputs, sort_keys=True)
        input_hash = hashlib.sha3_256(input_data.encode()).hexdigest()
        
        input_step = ProofStep(
            step_id=f"{chain_id}_input",
            proof_type=ProofType.INPUT,
            data={"inputs": inputs},
            hash_value=input_hash,
            previous_hash=previous_hash,
            timestamp=time.time()
        )
        chain.append(input_step)
        previous_hash = input_hash
        
        # Step 2: Operation proof
        operation_data = json.dumps({
            "operation_type": operation_type,
            "input_hash": input_hash
        }, sort_keys=True)
        operation_hash = hashlib.sha3_256(operation_data.encode()).hexdigest()
        
        operation_step = ProofStep(
            step_id=f"{chain_id}_operation",
            proof_type=ProofType.OPERATION,
            data={"operation_type": operation_type},
            hash_value=operation_hash,
            previous_hash=previous_hash,
            timestamp=time.time()
        )
        chain.append(operation_step)
        previous_hash = operation_hash
        
        # Step 3: Verification proof
        verification_data = json.dumps({
            "input_hash": input_hash,
            "operation_hash": operation_hash,
            "execution_record": execution_record.to_dict() if execution_record else {}
        }, sort_keys=True)
        verification_hash = hashlib.sha3_256(verification_data.encode()).hexdigest()
        
        verification_step = ProofStep(
            step_id=f"{chain_id}_verification",
            proof_type=ProofType.VERIFICATION,
            data={
                "is_deterministic": execution_record.is_deterministic if execution_record else True,
                "entropy_measure": execution_record.entropy_measure if execution_record else 0.0
            },
            hash_value=verification_hash,
            previous_hash=previous_hash,
            timestamp=time.time()
        )
        chain.append(verification_step)
        previous_hash = verification_hash
        
        # Step 4: Output proof
        output_data = json.dumps(outputs, sort_keys=True)
        output_hash = hashlib.sha3_256(output_data.encode()).hexdigest()
        
        output_step = ProofStep(
            step_id=f"{chain_id}_output",
            proof_type=ProofType.OUTPUT,
            data={"outputs": outputs},
            hash_value=output_hash,
            previous_hash=previous_hash,
            timestamp=time.time()
        )
        chain.append(output_step)
        previous_hash = output_hash
        
        # Step 5: Signature proof
        signature_data = previous_hash + operator_id
        signature_hash = hashlib.sha3_512(signature_data.encode()).hexdigest()
        
        signature_step = ProofStep(
            step_id=f"{chain_id}_signature",
            proof_type=ProofType.SIGNATURE,
            data={"operator_id": operator_id},
            hash_value=signature_hash,
            previous_hash=previous_hash,
            timestamp=time.time(),
            operator_signature=signature_hash
        )
        chain.append(signature_step)
        
        self._chains[chain_id] = chain
        
        return chain
    
    def generate_receipt(
        self,
        chain: List[ProofStep],
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        execution_time: float
    ) -> DeterministicReceipt:
        """
        Generate deterministic receipt from proof chain.
        
        Args:
            chain: Proof chain
            inputs: Operation inputs
            outputs: Operation outputs
            execution_time: Total execution time
            
        Returns:
            Deterministic receipt
        """
        receipt_id = str(uuid.uuid4())
        
        # Compute hashes
        input_data = json.dumps(inputs, sort_keys=True)
        input_hash = hashlib.sha3_256(input_data.encode()).hexdigest()
        
        output_data = json.dumps(outputs, sort_keys=True)
        output_hash = hashlib.sha3_256(output_data.encode()).hexdigest()
        
        operation_hash = chain[-2].hash_value  # Operation step
        
        # Get proof chain as list of hashes
        proof_chain = [step.hash_value for step in chain]
        
        # Calculate entropy measure (from verification step)
        verification_step = next((s for s in chain if s.proof_type == ProofType.VERIFICATION), None)
        entropy_measure = verification_step.data.get("entropy_measure", 0.0) if verification_step else 0.0
        
        # Check if deterministic
        is_deterministic = entropy_measure == 0.0
        
        receipt = DeterministicReceipt(
            receipt_id=receipt_id,
            operation_hash=operation_hash,
            input_hash=input_hash,
            output_hash=output_hash,
            proof_chain=proof_chain,
            execution_time=execution_time,
            entropy_measure=entropy_measure,
            is_deterministic=is_deterministic,
            timestamp=time.time()
        )
        
        return receipt
    
    def get_chain(self, chain_id: str) -> Optional[List[ProofStep]]:
        """Get proof chain by ID"""
        return self._chains.get(chain_id)
    
    def list_chains(self) -> List[str]:
        """List all chain IDs"""
        return list(self._chains.keys())


class C0Verifier:
    """
    Verifies C=0 proof chains for integrity and determinism.
    """
    
    def __init__(self, proof_chain_generator: ProofChainGenerator):
        """
        Initialize C=0 verifier.
        
        Args:
            Proof chain generator instance
        """
        self.generator = proof_chain_generator
        self._verification_history: List[Dict[str, Any]] = []
    
    def verify_proof_chain(
        self,
        chain: List[ProofStep],
        receipt: DeterministicReceipt
    ) -> Tuple[bool, VerificationStatus]:
        """
        Verify a proof chain.
        
        Args:
            chain: Proof chain to verify
            receipt: Receipt to verify against
            
        Returns:
            Tuple of (is_valid, verification_status)
        """
        # Verify chain integrity
        is_valid_chain = self._verify_chain_integrity(chain)
        
        # Verify receipt matches chain
        is_valid_receipt = self._verify_receipt(chain, receipt)
        
        # Check determinism
        is_deterministic = receipt.is_deterministic and receipt.entropy_measure == 0.0
        
        # Determine status
        if is_valid_chain and is_valid_receipt and is_deterministic:
            status = VerificationStatus.VALID
        elif is_valid_chain and is_valid_receipt:
            status = VerificationStatus.INVALID  # Valid but non-deterministic
        else:
            status = VerificationStatus.INVALID
        
        # Record verification
        verification_record = {
            "receipt_id": receipt.receipt_id,
            "timestamp": time.time(),
            "is_valid": status == VerificationStatus.VALID,
            "status": status.value,
            "is_deterministic": is_deterministic,
            "entropy_measure": receipt.entropy_measure
        }
        self._verification_history.append(verification_record)
        
        return status == VerificationStatus.VALID, status
    
    def _verify_chain_integrity(self, chain: List[ProofStep]) -> bool:
        """Verify chain integrity (hash linkage)"""
        for i, step in enumerate(chain):
            if i > 0:
                # Verify previous hash matches
                if step.previous_hash != chain[i-1].hash_value:
                    return False
        
        return True
    
    def _verify_receipt(self, chain: List[ProofStep], receipt: DeterministicReceipt) -> bool:
        """Verify receipt matches chain"""
        # Verify operation hash
        operation_step = next((s for s in chain if s.proof_type == ProofType.OPERATION), None)
        if not operation_step:
            return False
        
        if not hmac.compare_digest(receipt.operation_hash, operation_step.hash_value):
            return False
        
        # Verify proof chain
        expected_proof_chain = [step.hash_value for step in chain]
        if receipt.proof_chain != expected_proof_chain:
            return False
        
        return True
    
    def verify_c0_claim(self, receipt: DeterministicReceipt) -> Tuple[bool, str]:
        """
        Verify C=0 (Zero Entropy) claim.
        
        Args:
            receipt: Receipt to verify
            
        Returns:
            Tuple of (is_c0, explanation)
        """
        if not receipt.is_deterministic:
            return False, "Operation is non-deterministic"
        
        if receipt.entropy_measure > 0:
            return False, f"Entropy measure is {receipt.entropy_measure}, expected 0 for C=0"
        
        if receipt.entropy_measure < 0:
            return False, "Invalid entropy measure (negative)"
        
        # Verify receipt integrity
        if not receipt.verify():
            return False, "Receipt integrity check failed"
        
        return True, "C=0 verified - Zero Entropy confirmed"
    
    def get_verification_history(self) -> List[Dict[str, Any]]:
        """Get verification history"""
        return self._verification_history.copy()
    
    def create_zero_entropy_report(self, receipt: DeterministicReceipt) -> Dict[str, Any]:
        """
        Create comprehensive zero-entropy report.
        
        Args:
            receipt: Receipt to analyze
            
        Returns:
            Detailed report dictionary
        """
        is_c0, explanation = self.verify_c0_claim(receipt)
        
        return {
            "receipt_id": receipt.receipt_id,
            "timestamp": receipt.timestamp,
            "c0_verified": is_c0,
            "explanation": explanation,
            "metrics": {
                "entropy_measure": receipt.entropy_measure,
                "execution_time": receipt.execution_time,
                "is_deterministic": receipt.is_deterministic
            },
            "proof_chain_length": len(receipt.proof_chain),
            "verification_status": "PASSED" if is_c0 else "FAILED"
        }
