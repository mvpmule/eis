
from typing import List
import numpy as np
import httpx
from .protocol import split_input, combine_partials

class EISClient:
    def __init__(self, servers: List[str]):
        assert len(servers) >= 2, "Need at least two servers"
        self.servers = servers

    def remote_linear(self, x: np.ndarray, bias: np.ndarray | None = None) -> np.ndarray:
        shares = split_input(x.astype(np.float32), len(self.servers))
        partials = []
        with httpx.Client(timeout=30.0) as client:
            for server, share in zip(self.servers, shares):
                resp = client.post(f"{server}/matmul", json={"x_share": share.tolist()})
                resp.raise_for_status()
                y_part = np.array(resp.json()["y_partial"], dtype=np.float32)
                partials.append(y_part)
        y = combine_partials(partials, bias=bias)
        return y
