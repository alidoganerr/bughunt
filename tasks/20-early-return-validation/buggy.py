def check_rows(rows):
    """Return a list of problems found in rows (a list of dicts)."""
    problems = []
    for number, row in enumerate(rows, start=1):
        if not row.get("name"):
            problems.append("row %d: missing name" % number)
            return problems
        if row.get("qty", 0) < 0:
            problems.append("row %d: negative qty" % number)
    return problems
