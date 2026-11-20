# Parse CSV text

`parse_csv(text)` parses a string of standard CSV into a list of rows (each a list of strings).

- Fields are separated by commas. Rows end with `"\n"` or `"\r\n"`. A missing final line break is fine, and a final line break does not create an extra row.
- A field may be wrapped in double quotes. Inside quotes, commas are ordinary characters, a doubled quote (`""`) stands for one quote character, and line breaks belong to the field and are kept exactly as they appear in `text`.
- An empty line produces an empty row `[]`. Empty text produces `[]`.

## Example

```python
>>> parse_csv('id,note\r\n1,"first line\nsecond line"\r\n')
[['id', 'note'], ['1', 'first line\nsecond line']]
```
