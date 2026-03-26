"""Baseline backend application module."""


def health_status() -> dict[str, str]:
    """Return the service health status payload."""
    return {"status": "ok"}
