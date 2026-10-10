"""Math tools for Eggis: safe arithmetic and equation solving via sympy.

No eval(), no exec(). All expressions are parsed by sympy into its
own symbolic objects, evaluated only if they contain no free variables.
"""

from __future__ import annotations

from sympy import solve as sp_solve, Eq
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
import sympy as sp


_ALLOWED_NAMES = {
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "log": sp.log,
    "exp": sp.exp,
    "abs": sp.Abs,
    "factorial": sp.factorial,
    "pi": sp.pi,
    "e": sp.E,
}

_TRANSFORMS = (
    standard_transformations
    + (implicit_multiplication_application, convert_xor)
)


def _parse(expr_str: str):
    return parse_expr(
        expr_str,
        local_dict=_ALLOWED_NAMES,
        transformations=_TRANSFORMS,
        evaluate=True,
    )


def _format_number(value) -> str:
    """Render a sympy number as a clean string."""
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return str(value)

    if as_float.is_integer():
        return str(int(as_float))

    # Trim trailing zeros on non-integers.
    text = f"{as_float:.12g}"
    return text


def _handle_calc(expr_str: str) -> str:
    if not expr_str.strip():
        return "Usage: calc <expression>, for example: calc 2 + 2 * 5"
    try:
        expr = _parse(expr_str)
    except (SympifyError, SyntaxError, TypeError, ValueError) as exc:
        return f"I couldn't parse that expression: {exc}"

    free = expr.free_symbols
    if free:
        names = ", ".join(sorted(str(s) for s in free))
        return (
            f"That expression has unknown variables ({names}). "
            "Use 'solve <equation>' for equations with variables."
        )

    try:
        value = expr.evalf()
    except Exception as exc:  # noqa: BLE001
        return f"Evaluation failed: {exc}"

    return _format_number(value)


def _handle_solve(eq_str: str) -> str:
    if not eq_str.strip():
        return "Usage: solve <equation>, for example: solve 2*x + 3 = 11"
    try:
        if "=" in eq_str:
            left, right = eq_str.split("=", 1)
            expr = Eq(_parse(left), _parse(right))
        else:
            expr = Eq(_parse(eq_str), 0)
    except (SympifyError, SyntaxError, TypeError, ValueError) as exc:
        return f"I couldn't parse that equation: {exc}"

    symbols = sorted(expr.free_symbols, key=lambda s: str(s))
    if not symbols:
        return "That equation has no variables to solve for."

    try:
        solutions = sp_solve(expr, symbols)
    except Exception as exc:  # noqa: BLE001
        return f"Solve failed: {exc}"

    if not solutions:
        return "No solutions found."

    if isinstance(solutions, dict):
        parts = [f"{k} = {_format_number(v)}" for k, v in solutions.items()]
        return "; ".join(parts)

    if len(symbols) == 1:
        var = symbols[0]
        if isinstance(solutions, list):
            return f"{var} = " + ", ".join(_format_number(s) for s in solutions)
        return f"{var} = {_format_number(solutions)}"

    return str(solutions)


def handle_math_command(command: str) -> str | None:
    """Handle 'calc ...' and 'solve ...' commands.

    Returns a response string on match, or None if this isn't a math command.
    """
    text = command.strip()
    lower = text.lower()

    if lower.startswith("calc "):
        return _handle_calc(text[5:].strip())
    if lower == "calc":
        return "Usage: calc <expression>, for example: calc 2 + 2 * 5"

    if lower.startswith("solve "):
        return _handle_solve(text[6:].strip())
    if lower == "solve":
        return "Usage: solve <equation>, for example: solve 2*x + 3 = 11"

    return None
