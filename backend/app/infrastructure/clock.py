from time import monotonic


class MonotonicClock:
    """Unaffected by corrections to wall-clock time or timezone changes."""

    def now(self) -> float:
        return monotonic()
