from __future__ import annotations

from maven_agi.guardrails import SandboxFS
from maven_agi.tools.registry import default_registry


def test_calc():
    fs = SandboxFS("workspace_test")
    reg = default_registry(fs)
    calc = reg.get("calc")
    r = calc.run({"expr": "19*7+3"})
    assert r.ok
    assert r.output == "136"


def test_note_append(tmp_path):
    fs = SandboxFS(str(tmp_path))
    reg = default_registry(fs)
    note = reg.get("note_append")
    r = note.run({"text": "hello"})
    assert r.ok
    # notes.txt should exist
    content = fs.read_text("notes.txt")
    assert "hello" in content
