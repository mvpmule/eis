
import numpy as np

def demo_linear(d_in: int = 256, d_out: int = 10, seed: int = 42):
    rng = np.random.default_rng(seed)
    W = rng.normal(scale=0.1, size=(d_out, d_in)).astype(np.float32)
    b = rng.normal(scale=0.01, size=(d_out,)).astype(np.float32)
    return W, b
