from functools import wraps


def api_exempt(view_func):
    """ "Mark a view function as being exempt from login view protection"""

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.api_exempt = True
    return wraps(view_func)(wrapped_view)
