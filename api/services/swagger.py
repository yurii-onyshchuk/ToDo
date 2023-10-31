import functools


def swagger_safe(model):
    """Decorator for Django REST framework views to control the visibility of data in Swagger documentation.

    This decorator is used to ensure "Swagger safety" by allowing certain views to hide or replace data
    when generating Swagger documentation (or other documentation tools).
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(self, 'swagger_fake_view', False):
                return model.objects.none()
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
