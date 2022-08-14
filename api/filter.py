from enum import Enum

from typing import Optional


class Arithmetic:
    def __add__(self, other):  # operator +
        raise NotImplementedError

    def __radd__(self, other):  # operator +
        raise NotImplementedError

    def __sub__(self, other):  # operator -
        raise NotImplementedError

    def __rsub__(self, other):  # operator -
        raise NotImplementedError

    def __mul__(self, other):  # operator *
        raise NotImplementedError

    def __rmul__(self, other):  # operator *
        raise NotImplementedError

    def __truediv__(self, other):  # operator /
        raise NotImplementedError

    def __rtruediv__(self, other):  # operator /
        raise NotImplementedError

    def __floordiv__(self, other):  # operator //
        raise NotImplementedError

    def __rfloordiv__(self, other):  # operator //
        raise NotImplementedError

    def __mod__(self, other):  # operator %
        raise NotImplementedError

    def __rmod__(self, other):  # operator %
        raise NotImplementedError


# noinspection PyArgumentList
class LogicalOperator(Enum):
    EQUAL = "eq"
    NOT_EQUAL = "ne"

    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "ge"

    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "le"

    AND = "and"
    OR = "or"
    NOT = "not"


class Basic:

    def __init__(self, field):
        self.field: str = field  # First field
        self.logical_operator: Optional[LogicalOperator] = None  # Logical operator
        self.target: Optional[str] = None  # Value of field

    def __repr__(self):
        return f"{self.get_value()}"

    def get_value(self):
        return f"{self.field}"

    # Logical operators

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)

    def __invert__(self):
        raise NotImplementedError


class AndFilter(Basic):
    def __init__(self, base: Basic, other: Basic):
        super().__init__(base.get_value())
        self.logical_operator = LogicalOperator.AND
        self.target = other.get_value()

    def get_value(self):
        return f"{self.field} {self.logical_operator.value} {self.target}"


class OrFilter(Basic):
    def __init__(self, base: Basic, other: Basic):
        super().__init__(base.get_value())
        self.logical_operator = LogicalOperator.OR
        self.target = other.get_value()

    def get_value(self):
        return f"{self.field} {self.logical_operator.value} {self.target}"


class Filter(Basic):

    def get_value(self):
        if self.logical_operator is None:
            raise ValueError("Logical operator is not set")
        return f"{self.field} {self.logical_operator.value} '{self.target}'"

    # Logic operators

    def __eq__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.EQUAL
            f.target = other
            return f

        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.NOT_EQUAL
            f.target = other
            return f

        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.GREATER_THAN
            f.target = other
            return f

        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.GREATER_THAN_OR_EQUAL
            f.target = other
            return f

        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.LESS_THAN
            f.target = other
            return f

        raise NotImplementedError

    def __le__(self, other):
        if isinstance(other, (str, int)):
            f = Filter(self.field)
            f.logical_operator = LogicalOperator.LESS_THAN_OR_EQUAL
            f.target = other
            return f

        raise NotImplementedError


"""RouteName/Zh_tw eq '307' and StopName/Zh_tw eq '名來新城(中正路)'"""
