# Find a city

Write `find_city(cities, name)` in `solution.py`. It should return the first item of `cities` that matches `name`, or `None` if there is none. Two names match if they are equal after removing leading and trailing whitespace from both and ignoring letter case under full Unicode rules. For example, the German `"Weißenburg"` matches `"WEISSENBURG"`. The returned value is the original item from `cities`, unchanged.

## Example

```python
>>> find_city(["Berlin", "Weißenburg"], "WEISSENBURG")
'Weißenburg'
>>> find_city(["Berlin", "Weißenburg"], "  berlin ")
'Berlin'
```
