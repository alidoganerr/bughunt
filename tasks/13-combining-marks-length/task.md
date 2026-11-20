# Visible length

`visible_length(text)` returns the number of code points in `text` that are not combining marks. A code point is a combining mark if `unicodedata.combining(ch)` is non-zero. The text may be in any Unicode normal form, or in none, so `"\u00e9"` (U+00E9, one precomposed code point) and `"e\u0301"` (the letter e followed by U+0301, a combining acute accent) both have a visible length of 1. Code points whose combining class is zero always count, including emoji and CJK characters.

## Examples

```python
>>> visible_length("caf\u00e9")
4
>>> visible_length("cafe\u0301")
4
>>> visible_length("q\u0301")
1
```
