
# Encrypted Inference Streams (EIS)

**PoC**: Privacy-preserving fragmented inference for linear layers via additive secret sharing.

## What this is
A minimal, production-style repository that demonstrates client-side additive secret sharing for linear model inference across multiple untrusted servers. This is **not FHE** and **not MPC with full non-linear support** — it's a pragmatic split-compute for the linear parts of an inference graph (e.g., first projection of an embedding).

- Security: Each server receives a random share (x_i); without other shares, it learns nothing about x (information-theoretic for the linear leakage model).
- Utility: Servers apply the same linear operator W to their shares. The client sums partials to get W x (and adds bias locally).
- Demo: A toy classifier using two FastAPI servers; the client splits a 256-d vector, servers return W x_i, client recombines and finishes.

This PoC focuses on the first linear layer (or any linear subgraph) of a model. Extending through non-linearities requires additional protocols (e.g. Beaver triples, garbled circuits, or client-local non-linear steps).

## Repo layout
```
encrypted-inference-streams/
├─ eis/
│  ├─ __init__.py
│  ├─ crypto.py          # additive secret sharing over R^d
│  ├─ protocol.py        # split / combine utilities
│  ├─ server.py          # FastAPI app: POST /matmul  (returns W @ share)
│  ├─ client.py          # splits input, calls servers, recombines
│  ├─ models.py          # demo weight matrix, bias, helpers
├─ examples/
│  └─ run_demo.py        # start 2 servers + run a full client round-trip
├─ tests/
│  └─ test_crypto.py     # quick property tests
├─ README.md
├─ LICENSE
├─ THREAT_MODEL.md
├─ SECURITY.md
└─ requirements.txt
```

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Terminal 1: start server A
export EIS_PORT=8001
python -m eis.server

# Terminal 2: start server B
export EIS_PORT=8002
python -m eis.server

# Terminal 3: run the demo client (will call both servers)
python examples/run_demo.py --servers http://localhost:8001 http://localhost:8002
```

Expected output (abridged):
```
[Client] Ground truth logits  : [ ... ]
[Client] Fragmented logits    : [ ... ]
[Client] argmax matches? True
```

## How it works (math)

Given an input vector x ∈ R^d and a linear layer (W, b), split x into m additive shares:
x = x1 + x2 + ... + xm

Send each x_i to server i. Each server computes y_i = W x_i and returns it. The client recombines:
Σ y_i = Σ W x_i = W (Σ x_i) = W x
Then adds bias locally: y = Σ y_i + b, and continues with the rest of the model.

## Threat model (summary)
- Adversary: Any single server (or subset smaller than threshold) is honest-but-curious and does not collude.
- Guarantee: A single share is statistically independent from x. Without collusion, a server cannot reconstruct x.
- Limitations:
  - If servers collude and gather all shares, privacy is lost.
  - Linear side-channels (size, timing) remain; mitigate with padding and fixed shapes.
  - This PoC does not protect model weights on the server.
  - This PoC does not handle non-linear functions cryptographically; client performs non-linearities locally (or you need MPC/FHE add-ons).

See THREAT_MODEL.md for details.
