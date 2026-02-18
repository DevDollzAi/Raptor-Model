# Technical Architecture Overview

## The Logic-Compute Decoupling: Architectural Shift in Local Orchestration

The landscape of local large language model (LLM) deployment is undergoing a fundamental architectural transition characterized by the separation of application logic from inference compute. Historically, tools for running LLMs locally were designed as integrated packages where the user interface, model management, and tensor processing resided within a single process. This monolithic design created significant limitations, as the application's state was tied to the presence of a display and an active user session, preventing the inference engine from being treated as a persistent network resource.

### Component Architecture

| Component | Role in Logic-Compute Separation | Technical Impact |
|-----------|----------------------------------|------------------|
| **llmster Daemon** | Persistent background process managing system resources | Enables headless operation and remote compute availability |
| **lms CLI** | Control interface for model management and server states | Allows for automated scripting of model loads and unloads |
| **Local Server** | HTTP listener providing OpenAI-compatible endpoints | Decouples client-side code from physical hardware location |
| **Model Cache** | Local storage for GGUF weights and configuration metadata | Optimizes startup times through memory mapping (mmap) |
| **Runtime Engine** | Underlying llama.cpp 2.0 or MLX inference infrastructure | Governs raw throughput and parallel request handling |

### Performance Characteristics

The performance of the compute node is governed by the relationship between model parameter count, quantization depth, and the physical memory bandwidth of the GPU. LLMs are primarily memory-bandwidth bound rather than compute-bound during the inference phase, meaning the speed at which weights can be moved from VRAM to the processing cores is the limiting factor for tokens-per-second (TPS).

For 70B parameter models, exceeding dedicated memory capacity triggers a move to "Shared GPU Memory" or system RAM, resulting in a catastrophic collapse in performance—often dropping TPS from over 50 to sub-3.

## The Forge Layer: Hardware-Native Virtualization and Microvisor Isolation

The Forge layer represents the local virtualization engine of the workstation. True operator sovereignty requires a Type 1 bare-metal hypervisor architecture rather than a Type 2 hosted approach.

### Hypervisor Comparison

| Feature | Type 1 (Bare Metal) | Type 2 (Hosted) |
|---------|---------------------|-----------------|
| **Core Architecture** | Runs directly on hardware | Runs on top of host OS |
| **Security Posture** | Minimal attack surface | Vulnerable to host OS compromise |
| **Performance** | Near-native throughput | 15-30% overhead |
| **Resource Control** | Fine-grained, hardware-level | Abstracted by host OS kernel |
| **Deployment** | Data centers, AI clusters | Testing, educational labs |

### Xen Hypervisor: Microkernel Security

Xen is an open-source Type 1 hypervisor known for its microkernel design and robust isolation between virtual machines. The Xen architecture is built around a small, privileged domain called "dom0," which manages hardware and creates/controls unprivileged "domU" guest domains.

**Key Features:**
- Microkernel design (~1MB TCB)
- Driver isolation in dedicated VMs
- Strong security boundaries between domains
- Minimal attack surface

### KVM: Kernel Integration and Performance

KVM (Kernel-based Virtual Machine) integrates virtualization capabilities directly into the Linux kernel. By turning Linux into a hypervisor, KVM benefits from the extensive Linux ecosystem.

**Key Features:**
- Direct kernel scheduling and CPU pinning
- Superior CPU performance for AI workloads
- Integration with SELinux and sVirt
- Larger attack surface due to Linux dependency

## The Raptor Engine: Constrained Decoding and Token-Level Enforcement

The Raptor layer represents the task-specialized inference configuration of the workstation, utilizing JSON-structured behavior specifications known as "Cards".

### Base Model Specification

| Model Variant | MMLU (Gen. Knowledge) | MATH Benchmark | HumanEval (Coding) | SQL Accuracy |
|---------------|----------------------|----------------|-------------------|--------------|
| **Llama 3.1 70B** | Exceptional | High | High | ~85-92% |
| **Qwen 2.5 72B** | High | High | Elite | Elite |
| **Qwen 2.5-Coder-32B** | Competitive | 83.1 (Elite) | Very High | 95.73% |
| **GPT-4.5 Turbo** | Elite | Elite | Elite | <95.73% |

### Fine-Tuning Pipelines

**Direct Preference Optimization (DPO):**
- Eliminates need for explicit reward model
- Computationally lightweight
- Stable parameter adjustment based on pairwise comparisons
- Susceptible to overfitting in structured tasks

**Identity Preference Optimization (IPO):**
- Regularizes total preference score
- Prevents drift from base distribution
- Improves generalization across technical domains
- More stable than DPO for imperative outputs

### Grammar-Constrained Decoding (GCD)

GCD operates by applying parsing algorithms to the LLM's output in real time, building an automaton that interfaces with the decoding algorithm to mask away tokens that would lead to invalid states.

**Performance Characteristics:**
- Mask computations in ~50μs per token
- Compatible with 128k vocabularies
- Prevents malformed code generation
- Enables high-performance inference without quadratic scaling

## The Nest Layer: Storage Consistency and Data Integrity

The Nest layer serves as the block-based, hierarchical knowledge store of the workstation.

### ZFS vs Ceph Comparison

| Feature | ZFS (Local Storage) | Ceph (Distributed Storage) |
|---------|---------------------|---------------------------|
| **Core Focus** | Single-node performance | Massive scale-out |
| **Network Dependency** | None (purely local) | Critical (10GbE+ required) |
| **Snapshot Support** | Fully supported, integrated | Supported via RBD |
| **Complexity** | Simple setup and maintenance | Highly complex orchestration |
| **Fault Tolerance** | RAID-Z, mirroring | Multi-node replication |

### ZFS Architecture

**Copy-on-Write (CoW) Benefits:**
- Instantaneous, consistent snapshots
- Previous state never overwritten until new data verified
- Adaptive Replacement Cache (ARC) for aggressive RAM caching
- Dramatically improved read performance for RAG workloads

## The Hunt Layer: Networking and Isolation

The Hunt layer manages web ingestion and proactive monitoring, requiring absolute isolation between VMs on the single host.

### VXLAN for Logical Isolation

Traditional VLANs are constrained by a 12-bit ID space, limiting them to 4,096 segments. VXLAN addresses these limitations using a 24-bit identifier, supporting up to 16 million unique segments.

**Technical Implementation:**
- Layer 2 Ethernet frames encapsulated within Layer 3 UDP packets
- Overlay technology requiring no complex physical switching
- Enables dedicated networks for different task types
- Prevents lateral movement between compromised VMs

### Mesh VPN Architecture

**Tailscale Implementation:**
- Encrypted overlay network for device communication
- Direct communication without public internet exposure
- Authentication delegated to trusted Identity Providers
- Secure operator-to-workstation communication

## The Capability Lattice™: A New Economic Coordination Primitive

The Capability Lattice™ represents the functional apex of the Axiom Hive infrastructure, treating urban economies as live optimization surfaces over capabilities rather than static directories.

### Coordination Comparison

| Coordination Need | Traditional Platforms | Capability Lattice™ |
|-------------------|----------------------|-------------------|
| **Matching Model** | Categories to locations | Capabilities to constraints |
| **Information State** | Static directory attributes | Live optimization surface |
| **Optimization Level** | Entity-level (pairwise) | City-scale coordination |
| **Temporal Awareness** | Fixed listing hours | Live capacity vectors |

### Implementation Feasibility

As of February 2026, the implementation of the Capability Lattice™ is feasible due to:

1. **Managed Services**: Eliminated operational complexity in database administration
2. **Unified Technology Stacks**: Single language spanning entire architecture
3. **Computational Primitives**: Mature library functions for spatial indexing, temporal reasoning, and constraint satisfaction

## Security Hardening and the Locus-Operator Protocol (LOP)

The security of the workstation is anchored by the LOP, a unified cybernetic engine where logic, identity, and strategy converge into a single Single Source of Truth (SSOT).

### Neural Watermarking and Unforkability

**Stylometric Fingerprinting:**
- Embeds specific rhythm of sentence length, vocabulary density, and noun-verb ratios
- Survives copy-pasting and reformatting
- Permanent forensic link to the Locus of Origin
- "Syntactic DNA" for output verification

### Defensive Strategy: Moving Target Defense

**Strategic Flux Protocol:**
- Obfuscates core intent and strategy from external observers
- Projects multifaceted strategic outputs to mask singular hidden SSOT
- Makes it difficult for competitors to track search vectors or objectives

## Hardware Archetypes for Dedicating Compute Nodes

### NVIDIA RTX Series

**RTX 3090 (24GB):**
- Best value for local AI
- Two cards provide 48GB VRAM
- Enough for 70B parameter model at 4-bit quantization
- ~42 TPS for 70B models

**RTX 4090:**
- Up to 20% more throughput than 3090
- 52-65 TPS for 70B models
- Still requires second card for high-fidelity 70B operation

### Apple Silicon

**M2 Ultra (Mac Studio):**
- Unified memory architecture with up to 192GB
- Can load models impossible on consumer NVIDIA cards
- 405B parameter variant of Llama 3.1 support
- 40-100 TPS with massive context windows

### Hardware Profile Comparison

| Hardware Profile | Model Capacity | Token Speed (70B) | Advantage |
|------------------|----------------|-------------------|-----------|
| **RTX 4090** | High (24GB) | 52-65 tok/s | Absolute speed and CUDA ecosystem |
| **2x RTX 3090** | Extreme (48GB) | ~42 tok/s | Cost-effective 70B deployment |
| **Mac Studio M2 Ultra** | Unified (Up to 192GB) | ~40-100 tok/s | Large context and massive models |
| **RTX 3060 12GB** | Entry (12GB) | N/A (8B only) | Budget entry-level compute node |

## Conclusion

The technical architecture presented here provides a comprehensive framework for building sovereign cognitive infrastructure. By implementing these specifications, operators can achieve true sovereignty through deterministic AI, hardware-native virtualization, and city-scale economic coordination via the Capability Lattice™.