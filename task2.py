from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int   # 1 = найвищий
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def _validate_job(job: PrintJob) -> None:
    if job.volume <= 0:
        raise ValueError(f"Завдання {job.id}: volume має бути > 0")
    if job.print_time <= 0:
        raise ValueError(f"Завдання {job.id}: print_time має бути > 0")
    if job.priority not in (1, 2, 3):
        raise ValueError(f"Завдання {job.id}: priority має бути 1, 2 або 3")

def _batch_time(batch: List[PrintJob]) -> int:
    return max(job.print_time for job in batch)

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    jobs = [PrintJob(**j) for j in print_jobs]
    cons = PrinterConstraints(**constraints)

    if cons.max_volume <= 0 or cons.max_items <= 0:
        raise ValueError("Обмеження принтера мають бути > 0")

    for j in jobs:
        _validate_job(j)

    jobs.sort(key=lambda x: x.priority)

    print_order: List[str] = []
    total_time = 0

    current_batch: List[PrintJob] = []
    current_vol = 0.0

    def flush_batch():
        nonlocal current_batch, current_vol, total_time, print_order
        if not current_batch:
            return
        total_time += _batch_time(current_batch)

        print_order.extend([j.id for j in current_batch])
        current_batch = []
        current_vol = 0.0

    for job in jobs:

        if job.volume > cons.max_volume:
            flush_batch()

            total_time += job.print_time
            print_order.append(job.id)
            continue

        fits_items = (len(current_batch) + 1) <= cons.max_items
        fits_volume = (current_vol + job.volume) <= cons.max_volume

        if fits_items and fits_volume:
            current_batch.append(job)
            current_vol += job.volume
        else:
            flush_batch()
            current_batch.append(job)
            current_vol = job.volume

    flush_batch()

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# =========================
# Тестування
# =========================

def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

test_printing_optimization()
