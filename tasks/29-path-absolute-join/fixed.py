import posixpath


def upload_path(root, name):
    if not name:
        raise ValueError("name must not be empty")
    if name.startswith("/"):
        raise ValueError("name must be relative")
    if ".." in name.split("/"):
        raise ValueError("name must not contain '..'")
    return posixpath.join(root, name)
