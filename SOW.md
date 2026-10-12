# STATEMENT OF WORK (SOW) & TURNKEY DEPLOYMENT AGREEMENT

**Service:** Crucible-VM Hardware-Isolated Sandbox Deployment  
**Provider:** Gregg Bruce — Founder & Systems Architect, Crucible-VM  
**Client:** [Client Company Name] ("Client")  
**Effective Date:** [Date]  

---

## 1. Project Scope & Architecture

Provider will deliver a turnkey, hardware-isolated execution sandbox powered by Firecracker microVMs and KVM hardware virtualization on Client's dedicated cloud infrastructure.

### Technical Deliverables
1. **Hypervisor & Boundary Provisioning:**
   - Kernel-based Virtual Machine (KVM) acceleration verification and security hardening.
   - Firecracker jailer configuration with restricted seccomp syscall filters.
2. **Ephemeral Memory Storage:**
   - Dedicated RAM-backed filesystem (`tmpfs`) to prevent persistent disk leaks or host filesystem tampering by agent scripts.
3. **Execution Microservice Gateway:**
   - High-performance REST API (FastAPI) handling code execution payloads with cold boot and teardown latencies `< 1.5 seconds`.
   - Automated self-healing `systemd` daemon configured with auto-restart policies.
4. **Validation & Acceptance Test:**
   - Automated penetration and breakout containment test verifying zero host filesystem access.
   - Throughput validation benchmarking (~34,000 ops/s baseline).

---

## 2. Deployment Timeline & Access Requirements

* **Deployment Window:** Implementation will occur during a designated weekend window (Saturday or Sunday, 09:00 - 18:00 UTC).
* **Client Prerequisites:** Client shall provide temporary SSH root or sudo access to a dedicated Linux bare-metal or KVM-enabled cloud instance (Ubuntu 22.04/24.04 LTS on AWS bare-metal, Hetzner, or equivalent) 24 hours prior to scheduled setup.

---

## 3. Financial Terms & Payment Schedule

| Milestone | Amount (USD) | Payment Trigger |
| :--- | :--- | :--- |
| **Deposit (50%)** | **$1,750.00** | Due upon signature; prerequisite to release deployment date. |
| **Acceptance (50%)** | **$1,750.00** | Due upon successful verification of FastAPI health check and containment test. |
| **Total Turnkey Setup** | **$3,500.00** | **One-time fee** |

### Optional Continuous Engineering Retainer
* **Monthly Fee:** **$1,000.00 USD / month** (billed on the 1st of each month via Stripe/Wise).
* **Coverage:** Weekly guest kernel CVE vulnerability patches, memory tuning, and dedicated asynchronous support (Saturday maintenance window).

---

## 4. Acceptance & Signatures

Upon Client signature and deposit receipt, Provider will confirm the deployment date.

**CLIENT:**  
Authorized Signature: ___________________________________  
Printed Name: _________________________________________  
Title: _________________________________________________  
Date: __________________________________________________  

**PROVIDER:**  
Authorized Signature: *Gregg Bruce*  
Printed Name: Gregg Bruce  
Title: Founder & Systems Architect, Crucible-VM  
Date: [Date]  
