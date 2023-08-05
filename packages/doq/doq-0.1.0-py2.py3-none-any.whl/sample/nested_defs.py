def foo(arg1):
    """foo.

    :param arg1:
    """
    def bar(arg2):
        """bar.

        :param arg2:
        """
        pass


def bar(arg1=None):
    """bar.

    :param arg1:
    """
    def baz(arg2=None):
        """baz.

        :param arg2:
        """
        pass


def baz(arg1: str):
    """baz.

    :param arg1:
    :type arg1: str
    """
    def spam(arg2: str):
        """spam.

        :param arg2:
        :type arg2: str
        """
        pass


def spam(arg1: str = 'ham'):
    """spam.

    :param arg1:
    :type arg1: str
    """
    def foo(arg2: str = 'ham'):
        """foo.

        :param arg2:
        :type arg2: str
        """
        pass