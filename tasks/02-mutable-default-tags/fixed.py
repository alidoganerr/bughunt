def add_tag(tag, tags=None):
    """Return `tags` with the normalised `tag` added if it is new."""
    tag = tag.strip().lower()
    if not tag:
        raise ValueError("empty tag")
    result = list(tags) if tags is not None else []
    if tag not in result:
        result.append(tag)
    return result
