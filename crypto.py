
import numpy as np
from typing import List

def split_additive_shares(x: np.ndarray, m: int, rng: np.random.Generator | None = None) -> List[np.ndarray]:
    assert m >= 2, "Need at least 2 shares"
    rng = rng or np.random.default_rng()
    shares = [rng.normal(loc=0.0, scale=1.0, size=x.shape).astype(np.float32) for _ in range(m - 1)]
    last = (x.astype(np.float32) - np.sum(shares, axis=0)).astype(np.float32)
    shares.append(last)
    return shares

def recombine_shares(shares: List[np.ndarray]) -> np.ndarray:
    return np.sum(np.stack(shares, axis=0), axis=0).astype(np.float32)

def matmul_share(W: np.ndarray, x_share: np.ndarray) -> np.ndarray:
    return (W @ x_share).astype(np.float32)

def assert_privacy_single_share(x: np.ndarray, share: np.ndarray) -> float:
    x_flat = x.flatten()
    s_flat = share.flatten()
    if np.std(s_flat) < 1e-9 or np.std(x_flat) < 1e-9:
        return 0.0
    return float(np.corrcoef(x_flat, s_flat)[0, 1])
