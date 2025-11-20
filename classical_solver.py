from typing import List, Tuple
import itertools


def solve_schedule(
    drivers: List[str],
    routes: List[str],
    cost_matrix: List[List[float]],
) -> Tuple[List[Tuple[str, str, float]], float]:
    """
    Brute-force assignment: each driver gets exactly one route,
    each route gets exactly one driver. Small n only (3–5).
    """
    n_drivers = len(drivers)
    n_routes = len(routes)

    if n_drivers != n_routes:
        raise ValueError("For this demo, number of drivers must equal number of routes.")

    best_perm = None
    best_cost = float("inf")

    for perm in itertools.permutations(range(n_routes)):
        total = 0.0
        for i_driver, j_route in enumerate(perm):
            total += cost_matrix[i_driver][j_route]
        if total < best_cost:
            best_cost = total
            best_perm = perm

    assignments: List[Tuple[str, str, float]] = []
    for i_driver, j_route in enumerate(best_perm):
        assignments.append(
            (
                drivers[i_driver],
                routes[j_route],
                float(cost_matrix[i_driver][j_route]),
            )
        )

    return assignments, float(best_cost)
