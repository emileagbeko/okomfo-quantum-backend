import time
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import OptimizeRequest, OptimizeResponse, Assignment
from classical_solver import solve_schedule
from quantum_demo import run_quantum_demo

# CREATE THE APP FIRST
app = FastAPI(
    title="Okomfo Quantum Scheduler Backend",
    description="Hybrid classical + Guppy/Selene quantum demo for transport optimisation.",
    version="0.1.0",
)

# THEN ADD THE CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY — allows Supabase edge function to call
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"status": "okomfo-quantum-backend alive"}


@app.post("/optimize", response_model=OptimizeResponse)
def optimize(payload: OptimizeRequest) -> OptimizeResponse:
    """
    Hybrid endpoint:
    - classical brute-force assignment for small 3x3 demo
    - quantum teleportation demo via Guppy emulator (Selene-backed)
    """
    start = time.time()

    try:
        raw_assignments, total_cost = solve_schedule(
            payload.drivers,
            payload.routes,
            payload.cost_matrix,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    assignments: List[Assignment] = [
        Assignment(driver=d, route=r, cost=c) for d, r, c in raw_assignments
    ]

    quantum_sample, quantum_shots, qaoa_iterations, q_metadata = run_quantum_demo()

    exec_ms = int((time.time() - start) * 1000)

    return OptimizeResponse(
        success=True,
        method="hybrid_quantum_classical",
        assignments=assignments,
        total_cost=total_cost,
        execution_time_ms=exec_ms,
        quantum_sample=quantum_sample,
        quantum_shots=quantum_shots,
        qaoa_iterations=qaoa_iterations,
        quantum_metadata=q_metadata,
    )

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

