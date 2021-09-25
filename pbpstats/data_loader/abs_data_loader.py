from functools import wraps


def check_file_directory(method):
    """
    decorator to be used on method to load data from file to
    check that file directory is not None

    :raises: ValueError: If file_directory is None
    """

    @wraps(method)
    def decorated_method(self, *method_args, **method_kwargs):
        if self.file_directory is None:
            raise ValueError(f"file_directory cannot be None when data source is file")
        return method(self, *method_args, **method_kwargs)

    return decorated_method
