from typing import List


class Foo:
    """Foo."""

    def foo(self, arg1):
        """foo.

        :param arg1:
        """
        pass

    def bar(self, arg1=None):
        """bar.

        :param arg1:
        """
        pass

    def baz(self, arg1: str):
        """baz.

        :param arg1:
        :type arg1: str
        """
        pass

    def spam(self, arg1: str = 'ham'):
        """spam.

        :param arg1:
        :type arg1: str
        """
        pass

    def ham(self, arg1: str = 'ham') -> List[int]:
        pass
