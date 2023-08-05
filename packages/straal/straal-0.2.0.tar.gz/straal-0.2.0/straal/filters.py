import datetime
import enum
import functools
from typing import List


class Op(enum.Enum):
    Equal = "eq"
    NotEqual = "ne"
    Less = "lt"
    LessEqual = "le"
    Greater = "gt"
    GreaterEqual = "ge"


class FilterInstance:
    def __init__(self, name, operator: Op, value):
        self.name = name
        self._op = operator
        self._value = value

    def build_api_param(self):
        return {f"{self.name}__{self._op.value}": self._value}

    def __repr__(self):
        return f"{self.name} {self._op.name} {self._value}"


class Filter:
    ops: List[Op]

    def __init__(self, name):
        self._name = name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._define_requested_ops()

    @classmethod
    def _define_requested_ops(cls):
        for op in cls.ops:
            op_method = functools.partialmethod(cls.get_filter_instance, op=op)
            func_name = f"__{op.value}__"
            setattr(cls, func_name, op_method)

    def _filter_op_impl(self, value, op: Op):
        return self.get_filter_instance(value, op)

    def get_filter_instance(self, value, op: Op):
        return FilterInstance(self._name, op, value)

    def __eq__(self, value):
        raise NotImplementedError()

    def __ne__(self, value):
        raise NotImplementedError()

    def __lt__(self, value):
        raise NotImplementedError()

    def __le__(self, value):
        raise NotImplementedError()

    def __gt__(self, value):
        raise NotImplementedError()

    def __ge__(self, value):
        raise NotImplementedError()


class SimpleFilter(Filter):
    ops = [
        Op.Equal,
        Op.NotEqual,
        Op.Less,
        Op.LessEqual,
        Op.Greater,
        Op.GreaterEqual,
    ]


class DatetimeFilter(Filter):
    ops = [Op.Equal, Op.NotEqual, Op.Less, Op.LessEqual, Op.Greater, Op.GreaterEqual]

    def get_filter_instance(self, value: datetime.datetime, op: Op):
        aware_dt = value.replace(tzinfo=datetime.timezone.utc)
        timestamp = int(aware_dt.timestamp())
        return FilterInstance(self._name, op, timestamp)


class filters:
    ID = SimpleFilter(name="id")
    CreatedAt = DatetimeFilter(name="created_at")
    Email = SimpleFilter(name="email")
    Reference = SimpleFilter(name="reference")
