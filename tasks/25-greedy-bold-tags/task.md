# Bold text

Write `bold_texts(html)`. It returns a list with the text between each `<b>` and its closing `</b>`, in the order they appear. `<b>` elements are never nested, and the text inside them never contains `<` or a line break. Several elements may appear on one line. No `<b>` at all means `[]`.

```python
>>> bold_texts("<b>one</b> and <b>two</b>")
['one', 'two']
```
