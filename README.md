# tiny-duration-parse

Parse duration strings like `2h30m` into structured parts and render them back in canonical form.

```python
from tiny_duration_parse import parse, render

parts = parse("2h30m")
# {"h": 2, "m": 30}

print(render(parts))  # "2h30m"
```

## Why

You need to take a human-typed duration and turn it into something a program can reason about, then later print it back. This library does exactly that for the units `ms`, `s`, `m`, `h`, `d` — no more.

The trade-off: units are lowercase and case-sensitive. `2H30M` is rejected. This avoids the ambiguity where `M` could mean minutes or months, and keeps the parser dead simple. If you need weeks or months, this is not the right library.

## Edge cases

- Whitespace is rejected (`"2h 30m"` raises). Type your durations densely.
- Duplicate units are rejected (`"2h3h"` raises).
- Zero-value components are omitted on render (`{"h": 2, "m": 0}` renders as `"2h"`).
- `render({})` returns `"0s"` rather than the empty string, so you always get a valid duration back.
