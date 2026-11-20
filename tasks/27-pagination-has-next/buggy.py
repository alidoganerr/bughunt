def paginate(items, page, per_page):
    """Return one page of items (pages are numbered from 1)."""
    if page < 1 or per_page < 1:
        raise ValueError("page and per_page must be at least 1")
    start = (page - 1) * per_page
    return {
        "items": items[start:start + per_page],
        "page": page,
        "pages": -(-len(items) // per_page),
        "has_next": page * per_page <= len(items),
    }
