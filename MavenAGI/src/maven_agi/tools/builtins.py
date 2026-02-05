from __future__ import annotations

import ast
import operator as op
from typing import Dict

from maven_agi.guardrails import SandboxFS
from maven_agi.types import ToolResult


_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp):
        fn = _ALLOWED_OPS.get(type(node.op))
        if fn is None:
            raise ValueError("Operator not allowed.")
        return fn(_eval_expr(node.left), _eval_expr(node.right))
    if isinstance(node, ast.UnaryOp):
        fn = _ALLOWED_OPS.get(type(node.op))
        if fn is None:
            raise ValueError("Unary operator not allowed.")
        return fn(_eval_expr(node.operand))
    raise ValueError("Expression not allowed.")


def calc_tool(inp: Dict[str, object]) -> ToolResult:
    expr = str(inp.get("expr", "")).strip()
    if not expr:
        return ToolResult(ok=False, output="Missing 'expr'.")
    try:
        tree = ast.parse(expr, mode="eval")
        val = _eval_expr(tree.body)
        # Render int cleanly when possible
        if abs(val - int(val)) < 1e-12:
            out = str(int(val))
        else:
            out = str(val)
        return ToolResult(ok=True, output=out)
    except Exception as e:
        return ToolResult(ok=False, output=f"calc error: {e}")


def note_append_tool_factory(fs: SandboxFS):
    def _run(inp: Dict[str, object]) -> ToolResult:
        text = str(inp.get("text", "")).strip()
        if not text:
            return ToolResult(ok=False, output="Missing 'text'.")
        path = fs.append_text("notes.txt", text + "\n")
        return ToolResult(ok=True, output=f"saved to {path}")
    return _run


def write_file_tool_factory(fs: SandboxFS):
    def _run(inp: Dict[str, object]) -> ToolResult:
        path = str(inp.get("path", "")).strip()
        content = str(inp.get("content", ""))
        if not path:
            return ToolResult(ok=False, output="Missing 'path'.")
        full = fs.write_text(path, content)
        return ToolResult(ok=True, output=f"wrote {full}")
    return _run


def read_file_tool_factory(fs: SandboxFS):
    def _run(inp: Dict[str, object]) -> ToolResult:
        path = str(inp.get("path", "")).strip()
        if not path:
            return ToolResult(ok=False, output="Missing 'path'.")
        try:
            content = fs.read_text(path)
            return ToolResult(ok=True, output=content)
        except Exception as e:
            return ToolResult(ok=False, output=f"read error: {e}")
    return _run


def list_files_tool_factory(fs: SandboxFS):
    def _run(_: Dict[str, object]) -> ToolResult:
        files = fs.list_files()
        return ToolResult(ok=True, output="\n".join(files) if files else "(empty)")
    return _run


def http_get_stub(inp: Dict[str, object]) -> ToolResult:
    url = str(inp.get("url", "")).strip()
    if not url:
        return ToolResult(ok=False, output="Missing 'url'.")
    return ToolResult(ok=False, output="Network disabled in this template. Implement a real HTTP tool if needed.")
