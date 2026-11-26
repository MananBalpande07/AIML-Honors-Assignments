from functools import wraps
import time


def trace_execution(operation_tag):
    """Logs input arguments, keyword arguments, and return output of a function."""
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            arg_list = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
            formatted_args = ", ".join(arg_list)
            print(f"[TRACE | {operation_tag}] Executing {func.__name__}({formatted_args})")
            
            output = func(*args, **kwargs)
            
            print(f"[TRACE | {operation_tag}] Completed -> Output: {output}")
            return output
        return inner
    return decorator


def measure_latency(func):
    """Calculates and prints the execution time of the decorated function in milliseconds."""
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start_time) * 1000
        print(f"[METRICS] {func.__name__} executed in {duration_ms:.4f} ms")
        return result
    return inner


@trace_execution("TAX_CALC")
def calculate_net_amount(gross_amount, tax_rate=0.18):
    return round(gross_amount * (1 - tax_rate), 2)


@trace_execution("DISCOUNT_ENGINE")
def apply_bulk_discount(unit_price, quantity, discount_pct):
    total = unit_price * quantity
    return round(total - (total * discount_pct / 100), 2)


@measure_latency
@trace_execution("SERIES_COMPUTE")
def compute_geometric_sum(first_term, ratio, terms):
    if ratio == 1:
        return first_term * terms
    return first_term * (1 - ratio ** terms) / (1 - ratio)


@measure_latency
@trace_execution("FACTORIAL_GEN")
def calculate_factorial(n):
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    return fact


if __name__ == "__main__":
    print("=== Financial & Tax Operations (Logged) ===")
    calculate_net_amount(50000)
    calculate_net_amount(120000, tax_rate=0.12)
    apply_bulk_discount(1500, 10, 15)

    print("\n=== Heavy Computations (Logged + Timed) ===")
    compute_geometric_sum(2, 3, 12)
    calculate_factorial(15)