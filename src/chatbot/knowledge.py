# Raptor Chatbot Knowledge Base
# Domain knowledge about the Sovereign Shield system

"""
Structured knowledge base for the Raptor Model chatbot.
Contains information about all Sovereign Shield components and protocols.

Author: Nicholas Michael Grossi
"""

from typing import Dict, List, Tuple
import re


# ---------------------------------------------------------------------------
# Intent patterns: (compiled_regex, intent_label)
# ---------------------------------------------------------------------------
INTENT_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\b(hello|hi|hey|greet|good\s*(morning|afternoon|evening))\b", re.I), "greeting"),
    (re.compile(r"\b(bye|goodbye|see\s*you|exit|quit|close)\b", re.I), "farewell"),
    (re.compile(r"\b(help|what\s*can\s*you\s*(do|help)|commands?|options?|features?)\b", re.I), "help"),
    (re.compile(r"\b(bio[-\s]?hash|biohash|bio\s*hash\s*protocol)\b", re.I), "bio_hash"),
    (re.compile(r"\b(bark|behavioral\s*axiom|recursive\s*kernel|identity\s*violation)\b", re.I), "bark"),
    (re.compile(r"\b(inevitability\s*gate|five[- ]stage|liquidity\s*threshold|stage\s*[0-4])\b", re.I), "inevitability_gate"),
    (re.compile(r"\b(proof\s*chain|c\s*=\s*0|c=0|zero[- ]entropy|deterministic\s*verif)\b", re.I), "proof_chain"),
    (re.compile(r"\b(sovereign\s*shield|shield\s*status|shield\s*overview|what\s*is\s*raptor)\b", re.I), "shield_overview"),
    (re.compile(r"\b(did|decentralized\s*identifier|hd[- ]dis|identity\s*system)\b", re.I), "did"),
    (re.compile(r"\b(axiomhive|axiom\s*hive|deterministic\s*truth\s*engine)\b", re.I), "axiomhive"),
    (re.compile(r"\b(install|setup|how\s*to\s*(use|start|run|install|set\s*up))\b", re.I), "installation"),
    (re.compile(r"\b(config|configuration|settings?|parameter)\b", re.I), "configuration"),
    (re.compile(r"\b(register\s*node|wealth\s*node|node\s*registr)\b", re.I), "register_node"),
    (re.compile(r"\b(capital\s*flow|transfer|transact|payment|flow\s*vector)\b", re.I), "capital_flow"),
    (re.compile(r"\b(metric|health|hrl\s*score|shield\s*health|monitor)\b", re.I), "metrics"),
    (re.compile(r"\b(collapse\s*threshold|entropy\s*threshold|trigger|alert)\b", re.I), "collapse_thresholds"),
    (re.compile(r"\b(canary|shadow\s*(execut|host)|gradual\s*rollout)\b", re.I), "canary_shadow"),
    (re.compile(r"\b(lop|locus.of.origin|neural\s*watermark|attribution)\b", re.I), "lop"),
    (re.compile(r"\b(capability\s*lattice|grossi|city.scale|constraint\s*satisf)\b", re.I), "capability_lattice"),
    (re.compile(r"\b(ugw|utility\s*governance\s*weight|multi.hydro|token)\b", re.I), "ugw"),
    (re.compile(r"\b(ebpf|ring\s*0|kernel.level|enforcement)\b", re.I), "ebpf"),
    (re.compile(r"\b(thank|thanks|appreciate|great|awesome|perfect|nice)\b", re.I), "thanks"),
    (re.compile(r"\b(version|v\d+|release)\b", re.I), "version"),
    (re.compile(r"\b(example|demo|sample|show\s*me)\b", re.I), "example"),
    (re.compile(r"\b(architect|author|who\s*(built|made|created)|nicholas|alexis|grossi|adams)\b", re.I), "about_authors"),
]

# ---------------------------------------------------------------------------
# Response templates
# ---------------------------------------------------------------------------
RESPONSES: Dict[str, str] = {
    "greeting": (
        "👋 Hello! I'm the Raptor AI Assistant — your guide to the **Sovereign Shield** "
        "deterministic infrastructure protection system.\n\n"
        "I can help you with:\n"
        "• 🔐 Bio-Hash Protocol & identity management\n"
        "• 🔍 BARK Protocol & violation detection\n"
        "• 🚪 Inevitability Gate stages\n"
        "• ⛓️ C=0 Proof Chain verification\n"
        "• ⚙️ Configuration & installation\n"
        "• 💡 Code examples & usage\n\n"
        "What would you like to know?"
    ),

    "farewell": (
        "👋 Goodbye! The Sovereign Shield remains active. "
        "Stay deterministic — C=0 always."
    ),

    "thanks": (
        "You're welcome! The Sovereign Shield is here to ensure deterministic certainty. "
        "Is there anything else I can help you with?"
    ),

    "help": (
        "**Raptor Chatbot — Available Topics**\n\n"
        "🔐 **Identity & Cryptography**\n"
        "  • `bio-hash` — Bio-Hash Protocol & HD-DIS\n"
        "  • `DID` — Decentralized Identifiers\n"
        "  • `BARK` — Behavioral Axiom Recursive Kernel\n\n"
        "🚪 **Operation Control**\n"
        "  • `inevitability gate` — Five-stage liquidity system\n"
        "  • `proof chain` / `C=0` — Zero-entropy verification\n"
        "  • `canary` / `shadow` — Gradual rollout mechanisms\n\n"
        "💡 **Usage & Setup**\n"
        "  • `install` — Installation instructions\n"
        "  • `example` — Code examples\n"
        "  • `configuration` — Config options\n\n"
        "📊 **System**\n"
        "  • `metrics` — Shield health & HRL score\n"
        "  • `collapse thresholds` — Monitoring alerts\n"
        "  • `register node` — Wealth node registration\n"
        "  • `capital flow` — Transfer initiation\n\n"
        "🏗️ **Architecture**\n"
        "  • `AxiomHive` — Deterministic Truth Engine\n"
        "  • `capability lattice` — City-scale optimization\n"
        "  • `LOP` — Locus-Operator Protocol\n"
        "  • `eBPF` — Ring 0 enforcement\n"
        "  • `UGW` — Utility Governance Weight"
    ),

    "shield_overview": (
        "**🛡️ Sovereign Shield — Overview**\n\n"
        "The Raptor Model implements the **Sovereign Shield**: a deterministic infrastructure "
        "protection system designed to be immune to trust-collapse cascades that plague "
        "probabilistic systems.\n\n"
        "**Core Protocols:**\n"
        "1. 🔐 **Bio-Hash Protocol** — Cryptographic identity anchored to human operators via HD-DIS\n"
        "2. 🔍 **BARK Protocol** — Behavioral Axiom Recursive Kernel for identity violation detection\n"
        "3. 🚪 **Inevitability Gate** — Five-stage liquidity threshold control system\n"
        "4. ⛓️ **C=0 Proof Chain** — Zero-entropy deterministic verification\n\n"
        "**Key Properties:**\n"
        "• Cumulative error of zero (C=0) enforced\n"
        "• Cryptographic receipts for every operation\n"
        "• Sub-millisecond identity violation detection\n"
        "• Mathematical certainty in all operations\n\n"
        "Ask me about any specific protocol for details!"
    ),

    "bio_hash": (
        "**🔐 Bio-Hash Protocol (HD-DIS)**\n\n"
        "The Bio-Hash Protocol transforms simulated neural or motor trajectories into a "
        "proprietary cryptographic proof — the **Bio-Hash** — anchoring every operation "
        "to a verifiable human operator.\n\n"
        "**Components:**\n"
        "• `TrajectoryProcessor` — Projects trajectories into high-dimensional lattice space\n"
        "• `BioHashGenerator` — SHA3-512 hash generation from trajectory data\n"
        "• `DIDGenerator` — Creates Decentralized Identifiers (DIDs) bound to Bio-Hash\n"
        "• `HDIdentitySystem` — Full High-Dimensional Distributed Identity System\n\n"
        "**How it works:**\n"
        "```\n"
        "Trajectory Points → Lattice Projection (512D) → SHA3-512 Hash → DID Binding\n"
        "```\n\n"
        "**Quick usage:**\n"
        "```python\n"
        "from sovereign_shield import SovereignShield, TrajectoryPoint\n"
        "from sovereign_shield.bio_hash import TrajectoryType\n\n"
        "shield = SovereignShield(lattice_dimensions=512)\n"
        "trajectory = [\n"
        "    TrajectoryPoint(\n"
        "        coordinates=[0.1] * 512,\n"
        "        timestamp=1234567890.0,\n"
        "        trajectory_type=TrajectoryType.NEURAL_SIMULATION\n"
        "    )\n"
        "]\n"
        "node = shield.register_node('operator_001', trajectory, initial_balance=1000.0)\n"
        "print(f'DID: {node.did}')\n"
        "print(f'Bio-Hash: {node.bio_hash[:32]}...')\n"
        "```"
    ),

    "did": (
        "**🪪 Decentralized Identifiers (DIDs)**\n\n"
        "The Sovereign Shield uses the **HD-DIS** (High-Dimensional Distributed Identity System) "
        "to create DIDs that are cryptographically bound to Bio-Hash proofs.\n\n"
        "**DID Format:**\n"
        "```\n"
        "did:axiom:<24-character-identifier>\n"
        "```\n"
        "The identifier is derived from the operator's Bio-Hash and operator ID using SHA3-256.\n\n"
        "**DID Lifecycle:**\n"
        "1. Register identity with trajectory data\n"
        "2. DID generated and bound to Bio-Hash\n"
        "3. All operations reference the DID\n"
        "4. DID can be verified at any time\n\n"
        "**Verification:**\n"
        "```python\n"
        "from sovereign_shield.bio_hash import DIDGenerator\n\n"
        "gen = DIDGenerator(method='axiom')\n"
        "is_valid = gen.verify_did(did, expected_bio_hash, operator_id)\n"
        "```"
    ),

    "bark": (
        "**🔍 BARK Protocol — Behavioral Axiom Recursive Kernel**\n\n"
        "BARK provides sub-millisecond detection of identity violations using fixed-point "
        "convergence validation. It ensures the mathematical integrity of all operator identities.\n\n"
        "**Components:**\n"
        "• `BARKValidator` — Main validation orchestrator\n"
        "• `IdentityViolationDetector` — Detects trajectory anomalies\n"
        "• `AxiomValidator` — Validates system axiom statements\n"
        "• `FixedPointConvergence` — Mathematical convergence analysis\n\n"
        "**Fixed-Point Convergence:**\n"
        "BARK applies a system function `f(z, x)` iteratively until convergence:\n"
        "```\n"
        "z₀ = initial_trajectory\n"
        "zₙ₊₁ = f(zₙ, x)\n"
        "Converged when |zₙ₊₁ - zₙ| < tolerance\n"
        "```\n\n"
        "**Violation Detection:**\n"
        "```python\n"
        "violation = shield.detect_identity_violation(\n"
        "    node_id='node_001',\n"
        "    trajectory=[0.1, 0.2, 0.3],\n"
        "    statements={'axiom_1': 'operator must be verified'}\n"
        ")\n"
        "if violation:\n"
        "    print(f'Violation: {violation.violation_type}')\n"
        "    # Node automatically quarantined\n"
        "```"
    ),

    "inevitability_gate": (
        "**🚪 Inevitability Gate — Five-Stage Liquidity System**\n\n"
        "The Inevitability Gate is a progressive five-stage validation system that controls "
        "capital flow and ensures every operation passes mathematical verification.\n\n"
        "**The Five Stages:**\n\n"
        "**Stage 0: DID Registration & Bio-Hash Generation**\n"
        "  → Identity anchored cryptographically\n\n"
        "**Stage 1: BARK Validation (Fixed-Point Convergence)**\n"
        "  → Mathematical integrity verified\n\n"
        "**Stage 2: Auditor Review (Human-in-the-loop)**\n"
        "  → Human oversight (default: 5 min review window)\n\n"
        "**Stage 3: Canary Release (Gradual rollout)**\n"
        "  → 1% traffic tested first\n\n"
        "**Stage 4: Shadow Execution (Parallel validation)**\n"
        "  → Parallel execution on 3 shadow hosts\n\n"
        "**Configuration:**\n"
        "```python\n"
        "from sovereign_shield import InevitabilityGateConfig\n\n"
        "gate_config = InevitabilityGateConfig(\n"
        "    auditor_review_time=300.0,   # 5 minutes\n"
        "    canary_percentage=0.01,       # 1%\n"
        "    num_shadow_hosts=3\n"
        ")\n"
        "```"
    ),

    "proof_chain": (
        "**⛓️ C=0 Proof Chain — Zero-Entropy Verification**\n\n"
        "The C=0 Proof Chain ensures mathematical certainty in all operations by generating "
        "cryptographic receipts that prove zero cumulative error.\n\n"
        "**Components:**\n"
        "• `ProofChainGenerator` — Creates immutable proof chains\n"
        "• `C0Verifier` — Verifies C=0 condition on operations\n"
        "• `ZeroEntropyExecutor` — Executes operations with zero entropy\n"
        "• `DeterministicReceipt` — Immutable operation receipts\n\n"
        "**AxiomShard Hash:**\n"
        "```\n"
        "H_output = SHA-256(output || H_input || H_model || timestamp)\n"
        "```\n\n"
        "**Every receipt contains:**\n"
        "• Full cryptographic lineage back to origin\n"
        "• Input/output hash pairs\n"
        "• Temporal anchor (timestamp)\n"
        "• Cumulative error score (C=0 means zero errors)\n\n"
        "**Properties:**\n"
        "• Immutable — cannot be altered after creation\n"
        "• Auditable — full chain of custody\n"
        "• Zero-entropy — deterministic execution guaranteed"
    ),

    "axiomhive": (
        "**🏗️ AxiomHive — Deterministic Truth Engine**\n\n"
        "AxiomHive is the core infrastructure that enforces the **Zero Entropy Law (ZEL)**: "
        "if a computational sequence cannot be mathematically proven correct, it is blocked.\n\n"
        "**Core Laws:**\n"
        "• **Zero Entropy Law (ZEL)** — Only provably correct operations execute\n"
        "• **Proof-of-Invariance (PoI)** — Inductive proofs across all state transitions\n"
        "• **Q32 Fixed-Point Numerics** — Eliminates floating-point drift\n\n"
        "**Architecture:**\n"
        "• Ring 0 eBPF enforcement at kernel level\n"
        "• Deterministic Coherence Gate (DCG) on every state transition\n"
        "• AxiomShard cryptographic receipts for all outputs\n"
        "• Neural Watermarking via Locus-Operator Protocol (LOP)\n\n"
        "**Comparison:**\n"
        "| | Probabilistic AI | AxiomHive |\n"
        "|--|--|--|\n"
        "| Error floor | ~4% permanent | C=0 enforced |\n"
        "| Verification | Human-in-loop | Amortized to zero |\n"
        "| Output | Probability distributions | Cryptographic receipts |"
    ),

    "installation": (
        "**⚙️ Installation Guide**\n\n"
        "**Prerequisites:** Python ≥ 3.8, pip\n\n"
        "**Option 1 — From Source:**\n"
        "```bash\n"
        "git clone https://github.com/DevDollzAi/Raptor-Model.git\n"
        "cd Raptor-Model\n"
        "pip install -e .\n"
        "```\n\n"
        "**Option 2 — With dev dependencies:**\n"
        "```bash\n"
        "pip install -e '.[dev]'\n"
        "```\n\n"
        "**Launch the Chatbot:**\n"
        "```bash\n"
        "python chatbot_app.py\n"
        "# Then open http://localhost:5000 in your browser\n"
        "```\n\n"
        "**Dependencies:**\n"
        "• `numpy >= 1.20.0` — Numerical computations\n"
        "• `flask >= 3.0.0` — Web server for chatbot UI\n"
        "• `flask-cors >= 4.0.0` — Cross-origin support"
    ),

    "configuration": (
        "**⚙️ Configuration Options**\n\n"
        "**Quick configurations:**\n"
        "```python\n"
        "from sovereign_shield import ShieldConfig\n\n"
        "# Production (strict)\n"
        "config = ShieldConfig.production()\n"
        "# lattice_dimensions=1024, auditor_review_time=600s\n\n"
        "# Development (relaxed)\n"
        "config = ShieldConfig.development()\n"
        "# lattice_dimensions=256, auditor_review_time=60s\n"
        "```\n\n"
        "**Custom configuration:**\n"
        "```python\n"
        "from sovereign_shield import ShieldConfig, BioHashConfig, InevitabilityGateConfig\n\n"
        "config = ShieldConfig(\n"
        "    bio_hash=BioHashConfig(\n"
        "        lattice_dimensions=512,\n"
        "        did_method='axiom'\n"
        "    ),\n"
        "    gate=InevitabilityGateConfig(\n"
        "        auditor_review_time=300.0,\n"
        "        canary_percentage=0.01,\n"
        "        num_shadow_hosts=3\n"
        "    ),\n"
        "    enable_auto_verification=True\n"
        ")\n"
        "```"
    ),

    "register_node": (
        "**📝 Registering a Wealth Node**\n\n"
        "A wealth node is a protected entity in the Sovereign Shield. Registering "
        "a node creates a cryptographic identity and enables protected transactions.\n\n"
        "```python\n"
        "from sovereign_shield import SovereignShield\n"
        "from sovereign_shield.bio_hash import TrajectoryPoint, TrajectoryType\n\n"
        "# Initialize shield\n"
        "shield = SovereignShield(lattice_dimensions=512)\n\n"
        "# Define operator trajectory\n"
        "trajectory = [\n"
        "    TrajectoryPoint(\n"
        "        coordinates=[0.1, 0.2, 0.3] + [0.0] * 509,\n"
        "        timestamp=1234567890.0,\n"
        "        trajectory_type=TrajectoryType.NEURAL_SIMULATION,\n"
        "        metadata={'source': 'biometric_sensor'}\n"
        "    )\n"
        "]\n\n"
        "# Register node\n"
        "node = shield.register_node(\n"
        "    operator_id='operator_001',\n"
        "    trajectory=trajectory,\n"
        "    initial_balance=10000.0,\n"
        "    metadata={'tier': 'gold'}\n"
        ")\n\n"
        "print(f'Node ID: {node.node_id}')\n"
        "print(f'DID: {node.did}')\n"
        "print(f'Status: {node.status}')\n"
        "```\n\n"
        "**Node statuses:** `PROTECTED`, `EXPOSED`, `QUARANTINED`, `DEGRADED`"
    ),

    "capital_flow": (
        "**💸 Capital Flow Vectors**\n\n"
        "Capital flows are protected transfers between wealth nodes. Every flow "
        "passes through the full Inevitability Gate before execution.\n\n"
        "```python\n"
        "# Initiate transfer between nodes\n"
        "is_approved, execution_id = shield.initiate_capital_flow(\n"
        "    source_node_id=source.node_id,\n"
        "    target_node_id=target.node_id,\n"
        "    amount=500.0,\n"
        "    metadata={'purpose': 'service_payment'}\n"
        ")\n\n"
        "if is_approved:\n"
        "    print(f'Transfer approved: {execution_id}')\n"
        "    # Check receipt\n"
        "    flow = shield.get_capital_flow(execution_id)\n"
        "    print(f'Receipt: {flow.receipt}')\n"
        "else:\n"
        "    print('Transfer rejected by Inevitability Gate')\n"
        "```\n\n"
        "**Flow statuses:** `pending`, `approved`, `rejected`, `executed`\n\n"
        "Every executed flow generates an immutable **C=0 proof receipt**."
    ),

    "metrics": (
        "**📊 Shield Health & Metrics**\n\n"
        "The HRL (Health/Resilience/Liquidity) score tracks overall shield health.\n\n"
        "```python\n"
        "metrics = shield.get_metrics()\n\n"
        "print(f'Total nodes: {metrics.total_nodes}')\n"
        "print(f'Protected: {metrics.protected_nodes}')\n"
        "print(f'Exposed: {metrics.exposed_nodes}')\n"
        "print(f'Total value locked: {metrics.total_value_locked}')\n"
        "print(f'HRL Score: {metrics.hrl_score:.4f}')\n"
        "print(f'Triggered thresholds: {metrics.collapse_thresholds_triggered}')\n"
        "```\n\n"
        "**HRL Score Formula:**\n"
        "```\n"
        "HRL = (protected_nodes / total_nodes) × min(1.0, TVL / 1,000,000)\n"
        "```\n\n"
        "**Shield Status Values:**\n"
        "• `ACTIVE` — Normal operation\n"
        "• `COMPROMISED` — Threshold breached\n"
        "• `LOCKED` — Emergency lockdown\n"
        "• `MAINTENANCE` — Scheduled maintenance\n"
        "• `INITIALIZING` — Starting up"
    ),

    "collapse_thresholds": (
        "**⚠️ Collapse Thresholds**\n\n"
        "The shield monitors five critical metrics and triggers alerts when thresholds are crossed:\n\n"
        "| Threshold | Warning | Critical |\n"
        "|-----------|---------|----------|\n"
        "| `system_entropy` | 0.30 | 0.50 |\n"
        "| `identity_violations` | 2 | 5 |\n"
        "| `execution_latency_ms` | 2000ms | 5000ms |\n"
        "| `operation_failure_rate` | 5% | 10% |\n"
        "| `liquidity_ratio` | 0.30 | 0.20 |\n\n"
        "**Checking thresholds:**\n"
        "```python\n"
        "triggered = shield.check_collapse_thresholds({\n"
        "    'system_entropy': 0.45,\n"
        "    'identity_violations': 3,\n"
        "    'execution_latency_ms': 1500,\n"
        "    'operation_failure_rate': 0.03,\n"
        "    'liquidity_ratio': 0.35\n"
        "})\n"
        "if triggered:\n"
        "    print(f'ALERT: {triggered}')\n"
        "    # Shield status → COMPROMISED\n"
        "```\n\n"
        "If any critical threshold triggers, `shield.status` is set to `COMPROMISED`."
    ),

    "canary_shadow": (
        "**🐦 Canary & Shadow Execution**\n\n"
        "Stages 3 and 4 of the Inevitability Gate provide safe rollout mechanisms:\n\n"
        "**Stage 3 — Canary Release:**\n"
        "• Routes a small percentage (default 1%) of traffic through first\n"
        "• Validates behavior on real operations before full rollout\n"
        "• Configurable via `canary_percentage` parameter\n\n"
        "**Stage 4 — Shadow Execution:**\n"
        "• Runs operation in parallel on N shadow hosts (default: 3)\n"
        "• All shadow results must agree before proceeding\n"
        "• Provides consensus validation without affecting production\n\n"
        "**Configuration:**\n"
        "```python\n"
        "shield = SovereignShield(\n"
        "    canary_percentage=0.01,   # 1% canary\n"
        "    num_shadow_hosts=3        # 3 shadow hosts\n"
        ")\n"
        "```\n\n"
        "This mirrors production safety patterns used in large-scale deployments, "
        "ensuring zero-downtime, mathematically verified rollouts."
    ),

    "lop": (
        "**🔏 Locus-Operator Protocol (LOP)**\n\n"
        "The LOP ensures **unforkable attribution** — every output is permanently "
        "watermarked with its originator's cryptographic identity.\n\n"
        "**Properties:**\n"
        "• Neural Watermarking embedded in every computation\n"
        "• Locus of Origin (LOO) cryptographically bound to outputs\n"
        "• Self-rejecting: severed lineage triggers immediate operational collapse\n"
        "• Unforkable — cannot be replicated without the originating BMI binding\n\n"
        "**Semantic Syntax Enforcement:**\n"
        "The LOP enforces precise semantic meaning in all outputs, preventing:\n"
        "• Adversarial reinterpretation of results\n"
        "• Attribution spoofing\n"
        "• Lineage forgery\n\n"
        "**Integration:** The DCG (Deterministic Coherence Gate) checks LOP watermarks "
        "on every state transition, terminating any process that fails lineage verification."
    ),

    "capability_lattice": (
        "**🗺️ Capability Lattice — City-Scale Optimization**\n\n"
        "Designed by Nicholas Michael Grossi, the Capability Lattice models cities as "
        "dynamic, high-dimensional optimization surfaces over physical capabilities.\n\n"
        "**Core Resolution:**\n"
        "```\n"
        "Entity E can deliver outcome O at time t with confidence p ≥ 0.98\n"
        "```\n\n"
        "**Capabilities:**\n"
        "• **Live Capability Surfaces** — Real-time city capability modeling\n"
        "• **Multi-Leg Coordination** — Complex logistics as unified constraint satisfaction\n"
        "• **Temporal Arbitrage** — Time as a tradable capability dimension\n"
        "• **Mathematical Validation** — p ≥ 0.98 itinerary confidence\n\n"
        "**vs. Legacy Directories:**\n"
        "| | Legacy | Capability Lattice |\n"
        "|--|--|--|\n"
        "| Urban model | Static database | Live optimization surface |\n"
        "| Search | Sequential | Simultaneous constraint satisfaction |\n"
        "| Output | Candidate list | Validated itinerary |"
    ),

    "ugw": (
        "**⚖️ Utility Governance Weight (UGW)**\n\n"
        "UGW is the primary mechanism for allocating systemic authority proportional "
        "to verified operational utility.\n\n"
        "**UGW Computation:**\n"
        "```\n"
        "UGW = constraint_complexity + temporal_arbitrage_value + zero_entropy_efficiency\n"
        "```\n\n"
        "**4-Stage UGW Binding Protocol:**\n"
        "1. **PAS** — Phase Alignment Score validates capability claims\n"
        "2. **eBPF** — Ring 0 extracts unforgeable physical state telemetry\n"
        "3. **DCG** — Zero-error C=0 cryptographic hashing on execution\n"
        "4. **Multi-HYDRO** — UGW minted and distributed via ledger\n\n"
        "**Effect:** Entities with higher UGW are mathematically prioritized "
        "in future Capability Lattice resolutions, creating a positive feedback "
        "loop that rewards consistent, zero-entropy delivery."
    ),

    "ebpf": (
        "**🔒 Ring 0 eBPF Enforcement**\n\n"
        "AxiomHive enforces safety axioms at the kernel level using eBPF (extended "
        "Berkeley Packet Filter) programs running at Ring 0.\n\n"
        "**What this means:**\n"
        "• Safety rules are embedded in the OS kernel — not the application layer\n"
        "• **Physical incapability** — AI is structurally prevented from violating protocol\n"
        "• Bypasses application-layer filters entirely\n"
        "• Formally verified programs that cannot be overridden\n\n"
        "**Enforced by eBPF:**\n"
        "• Creator Lock — prevents unauthorized modifications\n"
        "• Sovereignty Deferral Module — enforces human authority\n"
        "• Substrate Ownership — prevents fork attacks\n\n"
        "**Security implication:** Competitors copying the application code lack "
        "the kernel-level substrate, causing inevitable degradation to a legacy system."
    ),

    "version": (
        "**📦 Raptor Model — Version Information**\n\n"
        "• **Sovereign Shield:** v1.0.0\n"
        "• **Raptor Chatbot:** v1.0.0\n"
        "• **Python:** ≥ 3.8 required\n"
        "• **numpy:** ≥ 1.20.0\n\n"
        "**System:** AxiomHive — Deterministic Truth Engine\n"
        "**Author:** Nicholas Michael Grossi — Capability Architect\n"
        "**Authority:** Alexis M. Adams — System Architect, AxiomHive Owner, LOP Authority"
    ),

    "about_authors": (
        "**👤 About the Creators**\n\n"
        "**Nicholas Michael Grossi — Capability Architect**\n"
        "• Author of the Capability Lattice System Design v1.0\n"
        "• Designer of the spatial capability solver and constraint satisfaction engine\n"
        "• Architect of the Sovereign Shield protocols\n\n"
        "**Alexis M. Adams — System Architect**\n"
        "• Owner of AxiomHive — Deterministic Truth Engine\n"
        "• LOP (Locus-Operator Protocol) Authority\n"
        "• Designer of the Zero Entropy Law and Proof-of-Invariance framework\n"
        "• Social Assurance Framework architect\n\n"
        "**AxiomHive** is the infrastructure layer unifying both systems into a "
        "city-scale deployment-ready platform."
    ),

    "example": (
        "**💡 Complete Usage Example**\n\n"
        "```python\n"
        "from sovereign_shield import SovereignShield\n"
        "from sovereign_shield.bio_hash import TrajectoryPoint, TrajectoryType\n\n"
        "# 1. Initialize shield\n"
        "shield = SovereignShield(\n"
        "    lattice_dimensions=512,\n"
        "    auditor_review_time=300.0,\n"
        "    canary_percentage=0.01,\n"
        "    num_shadow_hosts=3\n"
        ")\n\n"
        "# 2. Create trajectory data\n"
        "def make_trajectory(coords, ts):\n"
        "    return [TrajectoryPoint(\n"
        "        coordinates=coords,\n"
        "        timestamp=ts,\n"
        "        trajectory_type=TrajectoryType.NEURAL_SIMULATION\n"
        "    )]\n\n"
        "# 3. Register nodes\n"
        "alice = shield.register_node(\n"
        "    'alice', make_trajectory([0.1]*512, 1000.0), 5000.0\n"
        ")\n"
        "bob = shield.register_node(\n"
        "    'bob', make_trajectory([0.2]*512, 1001.0), 0.0\n"
        ")\n\n"
        "# 4. Initiate capital flow\n"
        "ok, exec_id = shield.initiate_capital_flow(\n"
        "    alice.node_id, bob.node_id, 100.0\n"
        ")\n"
        "print(f'Transfer approved: {ok}, ID: {exec_id}')\n\n"
        "# 5. Check metrics\n"
        "m = shield.get_metrics()\n"
        "print(f'HRL Score: {m.hrl_score:.4f}')\n"
        "print(f'TVL: {m.total_value_locked}')\n"
        "```"
    ),

    "default": (
        "I'm not sure I understood that. Here are some topics I can help with:\n\n"
        "• `bio-hash` — Cryptographic identity protocol\n"
        "• `BARK` — Identity violation detection\n"
        "• `inevitability gate` — Five-stage validation\n"
        "• `C=0 proof chain` — Zero-entropy verification\n"
        "• `install` — Setup instructions\n"
        "• `example` — Code examples\n"
        "• `help` — Full topic list\n\n"
        "Try asking something like: *\"How does the Bio-Hash Protocol work?\"* "
        "or *\"Show me a code example\"*"
    ),
}


def classify_intent(message: str) -> str:
    """
    Classify the intent of a user message.

    Args:
        message: Raw user message text

    Returns:
        Intent label string
    """
    for pattern, intent in INTENT_PATTERNS:
        if pattern.search(message):
            return intent
    return "default"


def get_response(intent: str) -> str:
    """
    Return the response text for a given intent.

    Args:
        intent: Intent label

    Returns:
        Response text (may contain Markdown)
    """
    return RESPONSES.get(intent, RESPONSES["default"])
