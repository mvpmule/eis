
import os
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .models import demo_linear
from .crypto import matmul_share

PORT = int(os.getenv("EIS_PORT", "8001"))
D_IN = int(os.getenv("EIS_D_IN", "256"))
D_OUT = int(os.getenv("EIS_D_OUT", "10"))
SEED = int(os.getenv("EIS_SEED", "42"))

W, b = demo_linear(D_IN, D_OUT, SEED)

class ShareRequest(BaseModel):
    x_share: list[float] = Field(..., description="Additive share of input vector")

class PartialResponse(BaseModel):
    y_partial: list[float]

app = FastAPI(title="EIS Server", version="0.1.0")

@app.post("/matmul", response_model=PartialResponse)
def matmul_endpoint(req: ShareRequest):
    x_share = np.array(req.x_share, dtype=np.float32)
    y_part = matmul_share(W, x_share)
    return PartialResponse(y_partial=y_part.tolist())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("eis.server:app", host="0.0.0.0", port=PORT, reload=False)
