def _hook_raise_errors(response, *args, **kwargs):
    """Response hook to raise exception for any HTTP error (status >= 400)."""
    response.raise_for_status()


class SessionErrorMixin(object):
    """A mixin for :class:`requests.Session` to raise exceptions for HTTP
    errors.
    """

    def __init__(self, **kwargs):
        super(SessionErrorMixin, self).__init__(**kwargs)
        self.hooks['response'].append(_hook_raise_errors)
