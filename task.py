from __future__ import annotations
from typing import List, Tuple

def minmax_divide_and_conquer(arr: List[float]) -> Tuple[float, float]:
    n = len(arr)
    if n == 0:
        raise ValueError("Empty array")
    if n == 1:
        return arr[0], arr[0]
    if n == 2:
        a, b = arr[0], arr[1]
        return (a, b) if a <= b else (b, a)

    mid = n // 2
    lmin, lmax = minmax_divide_and_conquer(arr[:mid])
    rmin, rmax = minmax_divide_and_conquer(arr[mid:])

    return lmin if lmin <= rmin else rmin, lmax if lmax >= rmax else rmax

arr = [7, -2, 15, 0, 9, 3, 3, -5, 11]
mn, mx = minmax_divide_and_conquer(arr)
print(f"Мінімум: {mn}, Максимум: {mx}")