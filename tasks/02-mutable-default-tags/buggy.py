"""Tag handling for a small note-taking tool."""


def add_tag(tag, tags=[]):
    """Return `tags` with the normalised `tag` added if it is new."""
    tag = tag.strip().lower()
    if not tag:
        raise ValueError("empty tag")
    if tag not in tags:
        tags.append(tag)
    return tags
