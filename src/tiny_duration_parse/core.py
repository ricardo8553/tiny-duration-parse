import re
from typing import Dict

# A unit is only valid if it maps to exactly one scaled number of seconds.
# ms, s, m, h, d were chosen because they are the common ISO-8601-like set
# and avoid spelling ambiguity (w for week vs word-initial w).
UNITS: Dict[str, int] = {
    "ms": 1,
    "s": 1000,
    "m": 60 * 1000,
    "h": 60 * 60 * 1000,
    "d": 24 * 60 * 60 * 1000,
}


class ParseError(ValueError):
    """Raised when a duration string cannot be parsed."""


_PART_RE = re.compile(
    r"(?P<num>\d+)(?P<unit>ms|s|m|h|d)",
)


def parse(duration: str) -> Dict[str, int]:
    """Parse a duration string like "2h30m" into a dict mapping unit -> count.

    Units are case-sensitive and lowercase only. Supported units:
    ms, s, m, h, d. Whitespace within the string is not permitted;
    we reject it to avoid silent truncation of malformed input.
    """
    if not isinstance(duration, str):
        raise ParseError("duration must be a str")
    if not duration:
        raise ParseError("empty duration")
    if duration.strip() != duration:
        raise ParseError("duration must not contain leading/trailing whitespace")
    if " " in duration:
        raise ParseError("duration must not contain interior whitespace")

    counts: Dict[str, int] = {}
    pos = 0
    while pos < len(duration):
        m = _PART_RE.match(duration, pos)
        if not m:
            raise ParseError(f"unexpected token at position {pos}: {duration[pos:]!r}")
        unit = m.group("unit")
        num = int(m.group("num"))
        if unit in counts:
            raise ParseError(f"duplicate unit {unit!r}")
        counts[unit] = num
        pos = m.end()

    if pos != len(duration):
        raise ParseError(f"unconsumed input at position {pos}")
    if not counts:
        raise ParseError("no components found")
    return counts


def render(parts: Dict[str, int]) -> str:
    """Render a parts dict back into the canonical string form.

    Order is always ms, s, m, h, d regardless of input order, so that
    render(parse(x)) is stable. Zero-value components are omitted.
    """
    if not isinstance(parts, dict):
        raise TypeError("parts must be a dict")
    result = []
    for unit in ("d", "h", "m", "s", "ms"):
        if unit not in parts:
            continue
        val = parts[unit]
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"value for {unit!r} must be int")
        if val < 0:
            raise ValueError(f"value for {unit!r} must be non-negative")
        if val == 0:
            continue
        result.append(f"{val}{unit}")
    return "".join(result) if result else "0s"
