import posixpath


def upload_path(root, name):
    if not name:
        raise ValueError("name must not be empty")
    if ".." in name.split("/"):
        raise ValueError("name must not contain '..'")
    return posixpath.join(root, name)
