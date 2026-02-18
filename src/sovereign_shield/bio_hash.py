# Bio-Hash Protocol Implementation
# High-Dimensional Distributed Identity System (HD-DIS)
# Cryptographic Identity Anchored to Human Operators

"""
The Bio-Hash Protocol implements cryptographic identity by transforming 
simulated neural or motor trajectories into a proprietary cryptographic 
proof called the Bio-Hash. This ensures every high-stakes operation is 
traceable to a verifiable human operator.

Key Components:
- TrajectoryProcessor: Transforms neural/motor trajectories into hashable data
- BioHashGenerator: Generates SHA3-512 hashes seeding cryptographic keys
- DIDGenerator: Creates Decentralized Identifiers bound to Bio-Hash
- HDIdentitySystem: High-Dimensional Distributed Identity System

Author: Nicholas Michael Grossi
"""

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
import numpy as np


class TrajectoryType(Enum):
    """Types of trajectories that can be processed"""
    NEURAL_SIMULATION = "neural_simulation"
    MOTOR_SEQUENCE = "motor_sequence"
    COGNITIVE_PATTERN = "cognitive_pattern"
    BIOMETRIC_SAMPLE = "biometric_sample"


@dataclass
class TrajectoryPoint:
    """A single point in a trajectory space"""
    coordinates: List[float]
    timestamp: float
    trajectory_type: TrajectoryType
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BioHashReceipt:
    """Receipt containing Bio-Hash proof and associated metadata"""
    bio_hash: str
    trajectory_hash: str
    did: str
    operator_id: str
    timestamp: float
    lattice_projection: List[float]
    proof_chain: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bio_hash": self.bio_hash,
            "trajectory_hash": self.trajectory_hash,
            "did": self.did,
            "operator_id": self.operator_id,
            "timestamp": self.timestamp,
            "lattice_projection": self.lattice_projection,
            "proof_chain": self.proof_chain
        }


class TrajectoryProcessor:
    """
    Processes simulated neural or motor trajectories into high-dimensional
    lattice projections for Bio-Hash generation.
    """
    
    def __init__(self, lattice_dimensions: int = 512):
        """
        Initialize trajectory processor.
        
        Args:
            lattice_dimensions: Number of dimensions in the high-dimensional lattice
        """
        self.lattice_dimensions = lattice_dimensions
    
    def process_trajectory(self, trajectory: List[TrajectoryPoint]) -> List[float]:
        """
        Project trajectory into high-dimensional lattice space.
        
        Args:
            trajectory: List of trajectory points
            
        Returns:
            High-dimensional lattice projection vector
        """
        if not trajectory:
            raise ValueError("Trajectory cannot be empty")
        
        # Initialize lattice projection
        lattice = np.zeros(self.lattice_dimensions)
        
        # Weight factors for temporal decay
        temporal_weights = self._compute_temporal_weights(trajectory)
        
        # Project each point into lattice space
        for i, point in enumerate(trajectory):
            if len(point.coordinates) > self.lattice_dimensions:
                coords = point.coordinates[:self.lattice_dimensions]
            else:
                coords = point.coordinates + [0.0] * (self.lattice_dimensions - len(point.coordinates))
            
            # Apply temporal weighting
            weighted_coords = np.array(coords) * temporal_weights[i]
            lattice += weighted_coords
        
        # Normalize to unit sphere
        norm = np.linalg.norm(lattice)
        if norm > 0:
            lattice = lattice / norm
        
        return lattice.tolist()
    
    def _compute_temporal_weights(self, trajectory: List[TrajectoryPoint]) -> List[float]:
        """Compute temporal decay weights for trajectory points"""
        if len(trajectory) == 1:
            return [1.0]
        
        weights = []
        base_time = trajectory[0].timestamp
        
        for point in trajectory:
            time_delta = point.timestamp - base_time
            # Exponential decay with half-life at midpoint
            weight = np.exp(-0.1 * time_delta)
            weights.append(weight)
        
        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]
    
    def compute_trajectory_hash(self, trajectory: List[TrajectoryPoint]) -> str:
        """
        Compute deterministic hash of trajectory data.
        
        Args:
            trajectory: List of trajectory points
            
        Returns:
            SHA3-256 hash of trajectory
        """
        # Sort by timestamp for deterministic ordering
        sorted_traj = sorted(trajectory, key=lambda p: p.timestamp)
        
        # Serialize trajectory
        data = b""
        for point in sorted_traj:
            coords_bytes = b",".join(str(c).encode() for c in point.coordinates)
            data += coords_bytes
            data += str(point.timestamp).encode()
            data += point.trajectory_type.value.encode()
        
        return hashlib.sha3_256(data).hexdigest()


class BioHashGenerator:
    """
    Generates Bio-Hash cryptographic proofs from trajectory data.
    Uses SHA3-512 for hash generation.
    """
    
    def __init__(self, trajectory_processor: TrajectoryProcessor):
        """
        Initialize Bio-Hash generator.
        
        Args:
            trajectory_processor: Trajectory processor instance
        """
        self.trajectory_processor = trajectory_processor
    
    def generate_bio_hash(
        self, 
        trajectory: List[TrajectoryPoint],
        operator_id: str,
        salt: Optional[bytes] = None
    ) -> str:
        """
        Generate Bio-Hash from trajectory data.
        
        The Bio-Hash is a SHA3-512 hash that seeds keys bound to a 
        Decentralized Identifier (DID).
        
        Args:
            trajectory: List of trajectory points
            operator_id: Unique identifier for the operator
            salt: Optional salt for additional randomness
            
        Returns:
            SHA3-512 Bio-Hash hexadecimal string
        """
        # Process trajectory into lattice projection
        lattice_projection = self.trajectory_processor.process_trajectory(trajectory)
        
        # Compute trajectory hash
        trajectory_hash = self.trajectory_processor.compute_trajectory_hash(trajectory)
        
        # Generate or use provided salt
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Prepare data for hashing
        hash_data = b""
        hash_data += trajectory_hash.encode()
        hash_data += operator_id.encode()
        hash_data += salt
        hash_data += b",".join(str(x).encode() for x in lattice_projection[:64])
        
        # Generate SHA3-512 Bio-Hash
        bio_hash = hashlib.sha3_512(hash_data).hexdigest()
        
        return bio_hash
    
    def generate_key_seed(self, bio_hash: str, key_type: str = "signing") -> bytes:
        """
        Generate cryptographic key seed from Bio-Hash.
        
        Args:
            bio_hash: Bio-Hash hexadecimal string
            key_type: Type of key to generate (signing, encryption, etc.)
            
        Returns:
            Deterministic key seed bytes
        """
        key_data = bio_hash.encode() + key_type.encode()
        return hashlib.sha3_256(key_data).digest()


class DIDGenerator:
    """
    Generates Decentralized Identifiers (DIDs) bound to Bio-Hash.
    """
    
    def __init__(self, method: str = "axiom"):
        """
        Initialize DID generator.
        
        Args:
            method: DID method identifier (default: axiom)
        """
        self.method = method
    
    def generate_did(self, bio_hash: str, operator_id: str) -> str:
        """
        Generate DID from Bio-Hash.
        
        DID format: did:method:unique-identifier
        
        Args:
            bio_hash: Bio-Hash hexadecimal string
            operator_id: Operator identifier
            
        Returns:
            Decentralized Identifier string
        """
        # Create unique identifier from Bio-Hash and operator
        identifier_data = bio_hash[:32] + operator_id[:16]
        identifier = hashlib.sha3_256(identifier_data.encode()).hexdigest()[:24]
        
        return f"did:{self.method}:{identifier}"
    
    def verify_did(self, did: str, expected_bio_hash: str, operator_id: str) -> bool:
        """
        Verify DID was generated from given Bio-Hash and operator.
        
        Args:
            did: DID to verify
            expected_bio_hash: Expected Bio-Hash
            operator_id: Expected operator
            
        Returns:
            True if DID is valid
        """
        expected_did = self.generate_did(expected_bio_hash, operator_id)
        return hmac.compare_digest(did, expected_did)


class HDIdentitySystem:
    """
    High-Dimensional Distributed Identity System (HD-DIS).
    
    Formalizes identity by transforming simulated neural or motor 
    trajectories into a proprietary cryptographic proof called the Bio-Hash.
    """
    
    def __init__(
        self,
        lattice_dimensions: int = 512,
        did_method: str = "axiom"
    ):
        """
        Initialize HD-DIS.
        
        Args:
            lattice_dimensions: Dimensions in high-dimensional lattice
            did_method: DID method to use
        """
        self.trajectory_processor = TrajectoryProcessor(lattice_dimensions)
        self.bio_hash_generator = BioHashGenerator(self.trajectory_processor)
        self.did_generator = DIDGenerator(did_method)
        
        # Store registered identities
        self._identities: Dict[str, BioHashReceipt] = {}
    
    def register_identity(
        self,
        trajectory: List[TrajectoryPoint],
        operator_id: str
    ) -> BioHashReceipt:
        """
        Register a new identity with the system.
        
        Args:
            trajectory: Trajectory data for the operator
            operator_id: Unique operator identifier
            
        Returns:
            Bio-Hash receipt with DID and proof chain
        """
        # Generate Bio-Hash
        bio_hash = self.bio_hash_generator.generate_bio_hash(trajectory, operator_id)
        
        # Compute trajectory hash
        trajectory_hash = self.trajectory_processor.compute_trajectory_hash(trajectory)
        
        # Generate DID
        did = self.did_generator.generate_did(bio_hash, operator_id)
        
        # Get lattice projection
        lattice_projection = self.trajectory_processor.process_trajectory(trajectory)
        
        # Generate proof chain
        proof_chain = self._generate_proof_chain(
            bio_hash, trajectory_hash, did, operator_id
        )
        
        # Create receipt
        receipt = BioHashReceipt(
            bio_hash=bio_hash,
            trajectory_hash=trajectory_hash,
            did=did,
            operator_id=operator_id,
            timestamp=time.time(),
            lattice_projection=lattice_projection,
            proof_chain=proof_chain
        )
        
        # Store identity
        self._identities[operator_id] = receipt
        
        return receipt
    
    def verify_identity(
        self,
        trajectory: List[TrajectoryPoint],
        operator_id: str
    ) -> Tuple[bool, Optional[BioHashReceipt]]:
        """
        Verify an operator's identity using trajectory data.
        
        Args:
            trajectory: Trajectory data to verify
            operator_id: Operator to verify
            
        Returns:
            Tuple of (is_valid, receipt_if_valid)
        """
        if operator_id not in self._identities:
            return False, None
        
        stored_receipt = self._identities[operator_id]
        
        # Generate Bio-Hash from provided trajectory
        current_bio_hash = self.bio_hash_generator.generate_bio_hash(
            trajectory, operator_id
        )
        
        # Compare hashes
        is_valid = hmac.compare_digest(current_bio_hash, stored_receipt.bio_hash)
        
        return is_valid, stored_receipt if is_valid else None
    
    def _generate_proof_chain(
        self,
        bio_hash: str,
        trajectory_hash: str,
        did: str,
        operator_id: str
    ) -> List[str]:
        """Generate proof chain for identity"""
        chain = []
        
        # Step 1: Trajectory hash
        chain.append(f"trajectory:{trajectory_hash}")
        
        # Step 2: Bio-Hash generation
        chain.append(f"bio_hash:{bio_hash[:32]}")
        
        # Step 3: DID binding
        chain.append(f"did:{did}")
        
        # Step 4: Operator binding
        chain.append(f"operator:{hashlib.sha3_256(operator_id.encode()).hexdigest()[:16]}")
        
        # Step 5: Timestamp anchor
        chain.append(f"timestamp:{int(time.time())}")
        
        return chain
    
    def get_identity(self, operator_id: str) -> Optional[BioHashReceipt]:
        """Get stored identity receipt"""
        return self._identities.get(operator_id)
    
    def list_identities(self) -> List[str]:
        """List all registered operator IDs"""
        return list(self._identities.keys())
