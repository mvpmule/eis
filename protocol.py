
from typing import List, Sequence
import numpy as np
from .crypto import split_additive_shares

def split_input(x: np.ndarray, m: int) -> List[np.ndarray]:
    return split_additive_shares(x, m)

def combine_partials(partials: Sequence[np.ndarray], bias: np.ndarray | None = None) -> np.ndarray:
    y = np.sum(np.stack(partials, axis=0), axis=0).astype(np.float32)
    if bias is not None:
        y = (y + bias.astype(np.float32)).astype(np.float32)
    return y
