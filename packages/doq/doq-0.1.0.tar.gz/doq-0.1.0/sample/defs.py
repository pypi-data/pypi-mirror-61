def foo():
    """foo."""
    pass


def bar(arg1):
    """bar.

    :param arg1:
    """
    pass


def baz(arg1=None):
    """baz.

    :param arg1:
    """
    pass


def spam(arg1: str):
    """spam.

    :param arg1:
    :type arg1: str
    """
    pass


def ham(arg1: str = 'ham'):
    """ham.

    :param arg1:
    :type arg1: str
    """
    pass


def bacon(arg1: str = 'spam', arg2: str = 'ham') -> int:
    """bacon.

    :param arg1:
    :type arg1: str
    :param arg2:
    :type arg2: str
    :rtype: int
    """
    pass