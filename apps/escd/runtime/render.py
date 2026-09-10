from html import escape
from typing import Any


def safe_text(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def render_job_row(job: dict[str, Any]) -> str:
    return (
        "<tr>"
        f"<td>{safe_text(job.get('title'))}</td>"
        f"<td>{safe_text(job.get('status'))}</td>"
        f"<td>{safe_text(job.get('updated_at'))}</td>"
        "</tr>"
    )
