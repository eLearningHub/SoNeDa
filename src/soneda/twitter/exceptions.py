"""Exceptions."""


class InvalidRequestError(Exception):
    """InvalidRequest."""

    ...


class UnauthorizedError(Exception):
    """Unauthorized."""

    ...


class MissingTokenError(Exception):
    """MissingToken."""

    ...


class MissingCredentialsError(Exception):
    """MissingCredentials."""

    ...
