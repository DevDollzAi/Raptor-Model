# Sovereign Shield Configuration
# Configuration defaults and settings

"""
Configuration defaults for the Sovereign Shield system.
These settings can be overridden when initializing the shield.

Author: Nicholas Michael Grossi
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class BioHashConfig:
    """Configuration for Bio-Hash Protocol"""
    lattice_dimensions: int = 512
    did_method: str = "axiom"
    trajectory_timeout: float = 30.0
    max_trajectory_points: int = 1000


@dataclass
class BARKConfig:
    """Configuration for BARK Protocol"""
    max_iterations: int = 1000
    convergence_tolerance: float = 1e-10
    divergence_threshold: float = 1e6
    custom_axioms: Optional[Dict[str, str]] = None


@dataclass
class InevitabilityGateConfig:
    """Configuration for Inevitability Gate"""
    auditor_review_time: float = 300.0  # 5 minutes
    canary_percentage: float = 0.01  # 1%
    num_shadow_hosts: int = 3
    auto_challenge: bool = True
    challenge_timeout: float = 600.0  # 10 minutes


@dataclass
class ProofChainConfig:
    """Configuration for C=0 Proof Chain"""
    fixed_point_precision: int = 18
    max_chain_length: int = 1000
    receipt_ttl: float = 86400.0  # 24 hours
    verify_on_create: bool = True


@dataclass
class ShieldConfig:
    """Main Sovereign Shield configuration"""
    bio_hash: BioHashConfig = field(default_factory=BioHashConfig)
    bark: BARKConfig = field(default_factory=BARKConfig)
    gate: InevitabilityGateConfig = field(default_factory=InevitabilityGateConfig)
    proof_chain: ProofChainConfig = field(default_factory=ProofChainConfig)
    
    # Collapse threshold settings
    collapse_thresholds: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "entropy_threshold": {"critical": 0.5, "warning": 0.3},
        "violation_threshold": {"critical": 5, "warning": 2},
        "latency_threshold": {"critical": 5000, "warning": 2000},
        "failure_threshold": {"critical": 0.1, "warning": 0.05},
        "liquidity_threshold": {"critical": 0.2, "warning": 0.3}
    })
    
    # General settings
    enable_auto_verification: bool = True
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "bio_hash": {
                "lattice_dimensions": self.bio_hash.lattice_dimensions,
                "did_method": self.bio_hash.did_method,
                "trajectory_timeout": self.bio_hash.trajectory_timeout,
                "max_trajectory_points": self.bio_hash.max_trajectory_points
            },
            "bark": {
                "max_iterations": self.bark.max_iterations,
                "convergence_tolerance": self.bark.convergence_tolerance,
                "divergence_threshold": self.bark.divergence_threshold
            },
            "gate": {
                "auditor_review_time": self.gate.auditor_review_time,
                "canary_percentage": self.gate.canary_percentage,
                "num_shadow_hosts": self.gate.num_shadow_hosts,
                "auto_challenge": self.gate.auto_challenge,
                "challenge_timeout": self.gate.challenge_timeout
            },
            "proof_chain": {
                "fixed_point_precision": self.proof_chain.fixed_point_precision,
                "max_chain_length": self.proof_chain.max_chain_length,
                "receipt_ttl": self.proof_chain.receipt_ttl,
                "verify_on_create": self.proof_chain.verify_on_create
            },
            "collapse_thresholds": self.collapse_thresholds,
            "enable_auto_verification": self.enable_auto_verification,
            "enable_metrics": self.enable_metrics,
            "log_level": self.log_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShieldConfig":
        """Create config from dictionary"""
        bio_hash = BioHashConfig(**data.get("bio_hash", {}))
        bark = BARKConfig(**data.get("bark", {}))
        gate = InevitabilityGateConfig(**data.get("gate", {}))
        proof_chain = ProofChainConfig(**data.get("proof_chain", {}))
        
        return cls(
            bio_hash=bio_hash,
            bark=bark,
            gate=gate,
            proof_chain=proof_chain,
            collapse_thresholds=data.get("collapse_thresholds", {}),
            enable_auto_verification=data.get("enable_auto_verification", True),
            enable_metrics=data.get("enable_metrics", True),
            log_level=data.get("log_level", "INFO")
        )
    
    @classmethod
    def production(cls) -> "ShieldConfig":
        """Production configuration with stricter settings"""
        config = cls()
        config.bio_hash.lattice_dimensions = 1024
        config.gate.auditor_review_time = 600.0  # 10 minutes
        config.gate.canary_percentage = 0.001  # 0.1%
        config.proof_chain.receipt_ttl = 259200.0  # 3 days
        config.log_level = "WARNING"
        return config
    
    @classmethod
    def development(cls) -> "ShieldConfig":
        """Development configuration with relaxed settings"""
        config = cls()
        config.bio_hash.lattice_dimensions = 256
        config.gate.auditor_review_time = 60.0  # 1 minute
        config.gate.canary_percentage = 0.05  # 5%
        config.proof_chain.receipt_ttl = 3600.0  # 1 hour
        config.log_level = "DEBUG"
        return config


# Default configuration instance
DEFAULT_CONFIG = ShieldConfig()

# Export configuration classes
__all__ = [
    "ShieldConfig",
    "BioHashConfig",
    "BARKConfig",
    "InevitabilityGateConfig",
    "ProofChainConfig",
    "DEFAULT_CONFIG"
]
