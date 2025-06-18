# tests/test_scenarios.py
#
# Run both example events and assert that the tutorial
# keeps working ( critical alert on event-1, nothing on event-2 ).
#
# Run with:  pytest -q
#
import io
from contextlib import redirect_stdout

from main import run_scenario


def _run(event_path: str) -> str:
    """Helper – capture stdout from run_scenario()."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        run_scenario(event_path)
    return buf.getvalue()


def test_event_1_triggers_alert():
    output = _run("events/event-1.txt")
    assert "CRITICAL ALERT" in output
    assert "No alerts generated" not in output


def test_event_2_generates_nothing():
    output = _run("events/event-2.txt")
    assert "No alerts generated." in output
    # safety-check that the critical message is absent
    assert "CRITICAL ALERT" not in output
