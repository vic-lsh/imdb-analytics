def singleton(cls, *args, **kwargs):
    """Class decorator that ensures decorated classes only have one instance."""

    instances = {}

    def singleton_wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return singleton_wrapper