from typing import List, Dict, Any
from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    drivers: List[str]
    routes: List[str]
    cost_matrix: List[List[float]]  # rows = drivers, cols = routes


class Assignment(BaseModel):
    driver: str
    route: str
    cost: float


class OptimizeResponse(BaseModel):
    success: bool
    method: str
    assignments: List[Assignment]
    total_cost: float
    execution_time_ms: int
    quantum_sample: str
    quantum_shots: int
    qaoa_iterations: int
    quantum_metadata: Dict[str, Any] = {}
