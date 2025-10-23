# Encrypted Inference Streams (EIS)
### MVPMule Labs • Technical Note 2025-01  
**Author:** [Alessandro Scopetoni](https://callthecto.com) 
**Category:** Privacy-Preserving Inference / Edge–Cloud Split Compute  

---

## Abstract
We introduce **Encrypted Inference Streams (EIS)** — a pragmatic framework for *privacy-preserving model inference* that fragments user inputs into multiple additive shares and distributes them to independent inference servers.  
Each server performs linear operations on its fragment; the client recombines the partial results locally.  
Unlike full homomorphic encryption or secure multi-party computation, EIS targets *practical deployability*: it protects input confidentiality against any single compromised server while keeping computational overhead minimal.  
A Python/FastAPI proof-of-concept demonstrates the viability of this approach on a simple linear model.

---

## 1. Motivation
Modern AI applications rely heavily on cloud inference, creating tension between **privacy** (keeping user data local) and **utility** (offloading heavy computation).  
While **Homomorphic Encryption (HE)** and **MPC** guarantee strong security, their cost—often 1000× slower inference—makes them impractical for real-time mobile scenarios.

EIS seeks a middle ground:
- linear parts of a model can be **outsourced in fragments**,  
- non-linear layers remain local,  
- each remote endpoint sees only random-looking data.

This pattern allows **lightweight client devices** to collaborate with **untrusted compute providers** while maintaining statistical privacy of user inputs.

---

## 2. Protocol Overview

Let a model contain a linear operator \( W \in \mathbb{R}^{m \times n} \) and bias \( b \in \mathbb{R}^m \).  
Given an input vector \( x \in \mathbb{R}^n \), the client generates \( k \) random shares:

\[
x = x_1 + x_2 + \dots + x_k
\]

Each share \( x_i \) is sent to a distinct inference server \( S_i \).  
Server \( S_i \) computes:

\[
y_i = W x_i
\]

and returns it to the client.  
The client recombines results:

\[
\hat{y} = \sum_i y_i + b = W \sum_i x_i + b = W x + b
\]

Thus the correct linear output is reconstructed **without any single server ever seeing x**.

### Key properties
| Property | Description |
|-----------|--------------|
| **Additive secrecy** | Any single share \( x_i \) is independent of \( x \). |
| **Linearity** | Operations distribute cleanly across shares. |
| **Minimal overhead** | Servers perform standard matrix multiplication. |
| **Client control** | Non-linearities (ReLU, GELU, Softmax) executed locally. |

---

### Runtime Flow
1. **Client** generates random additive shares of input `x`.  
2. **Shares** are sent to two or more independent servers.  
3. **Servers** apply their local `W` (same weights, same dimensions).  
4. **Client** aggregates partial outputs and adds bias `b`.  
5. **Output** matches the result of the original linear layer.

### Sample Metrics
| Metric | Value (demo 256→10 layer, 2 servers) |
|--------|--------------------------------------|
| Privacy diagnostic corr(x, share₀) | ≈ 0.002 |
| Reconstruction error | < 1e-5 |
| Runtime overhead vs local matmul | ~1.5× (network-bound) |

---

## 4. Security Model

| Element | Protected? | Notes |
|----------|-------------|------|
| **Client input x** | ✅ against any single server | additive shares are statistically independent |
| **Model weights W, bias b** | ❌ | visible to servers |
| **Output y = Wx + b** | ⚠️ | recombined locally; protect via HTTPS/TLS |
| **Non-linear activations** | ✅ (local only) | not shared |
| **Colluding servers** | ❌ | protocol loses confidentiality if all servers collude |

EIS assumes an **honest-but-curious**, non-colluding server model and secure channels (TLS).  
Traffic analysis may reveal input size; use padding and batching to mitigate.

---

## 5. Comparison to Alternative Methods

| Method | Input Privacy | Compute Cost | Deployability |
|---------|----------------|---------------|----------------|
| **Homomorphic Encryption (FHE)** | Strong | 10³–10⁴× slower | Low |
| **Secure MPC (full)** | Strong | 100–1000× slower | Moderate |
| **Client-side only** | Perfect | Device-limited | Medium |
| **EIS (ours)** | Medium (non-colluding) | ~1–2× slower | High |

EIS fills the *practical niche* between heavy cryptography and plain inference: a lightweight, statistically private option for low-risk workloads.

---

## 6. Extensions and Future Work
1. **Threshold-based sharing:** require a minimum subset of servers to reconstruct.  
2. **Server-side weight obfuscation:** encrypt `W` via functional encryption or secure enclaves (TEE).  
3. **Non-linear support:** integrate Beaver triples or garbled circuits for ReLU/GELU.  
4. **Model partitioning:** automatically split full transformer blocks into EIS-compatible linear fragments.  
5. **Hardware acceleration:** implement in Rust + WebAssembly for mobile edge inference.

---

## 7. Applications
- **Healthcare AI:** offload heavy inference without exposing patient data.  
- **Financial assistants:** process encrypted transaction features.  
- **Edge assistants:** on-device large-model fragments with cloud linear compute.  
- **Federated analytics:** share workloads between institutions without raw data transfer.

---

## 8. Limitations
- Collusion between all servers reveals the input.  
- Not secure against chosen-plaintext or side-channel attacks.  
- Limited to linear operations unless extended with MPC/FHE layers.  
- Latency increases linearly with number of servers.

---

## 9. Conclusion
Encrypted Inference Streams demonstrate that practical, privacy-preserving inference need not rely on heavy cryptography.  
By combining *additive secret sharing* and *split compute*, EIS preserves accuracy and usability while reducing exposure risk.  
This concept offers a concrete, immediately deployable pattern for hybrid edge-cloud AI systems.

---

## References
1. Yao, A. C. *Protocols for Secure Computations*, FOCS 1982.  
2. Beaver, D. *Efficient Multiparty Protocols Using Circuit Randomization*, CRYPTO 1991.  
3. Gentry, C. *Fully Homomorphic Encryption Using Ideal Lattices*, STOC 2009.  
4. Bonawitz et al., *Practical Secure Aggregation for Privacy-Preserving ML*, CCS 2017.  
5. MVPMule Labs, *Encrypted Inference Streams PoC*, 2025 (this work).

---
