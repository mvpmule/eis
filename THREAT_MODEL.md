
# Threat Model — Encrypted Inference Streams (EIS)

## Assets
- Client input vector x (private).
- Linear operator W and bias b (server-side; not protected by this PoC).
- Partial results y_i = W x_i (in transit).

## Adversaries & Assumptions
- Servers are independent and do not collude (honest-but-curious). Any single server may attempt to infer x.
- Network may be observable; use TLS in production.
- Client is trusted and performs recombination and any non-linear operations locally.

## Guarantees
- Input privacy against any single server: Each server receives a random share x_i such that x = Σ x_i. Marginally, x_i is independent of x. Thus x_i reveals no information about x without other shares.
- Computation privacy: A server computes W x_i. Without other shares, this is statistically independent from W x (up to distributional assumptions about x).

## Non-Goals / Limitations
- Collusion: If all servers collude and aggregate shares, x is revealed.
- Weight privacy: This PoC does not protect W or b from a malicious client.
- Non-linear ops: Not protected/outsourced here. Client should run them locally or use advanced MPC.
- Traffic analysis: Message size and timing may leak metadata. Use padding, batching, and fixed shapes.
