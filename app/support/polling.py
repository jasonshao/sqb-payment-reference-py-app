def build_polling_schedule(
    *,
    quick_phase_seconds: int,
    quick_interval_seconds: int,
    slow_interval_seconds: int,
    max_wait_seconds: int,
) -> list[int]:
    elapsed = 0
    schedule: list[int] = []
    while elapsed < max_wait_seconds:
        interval = quick_interval_seconds if elapsed < quick_phase_seconds else slow_interval_seconds
        schedule.append(interval)
        elapsed += interval
    return schedule
