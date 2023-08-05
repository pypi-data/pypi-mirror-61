class StraalError(Exception):
    _REGISTRY = {}

    def __init_subclass__(cls, code: int, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._register_straal_exc(code)

    @classmethod
    def _register_straal_exc(cls, code: int):
        if code in cls._REGISTRY:
            raise RuntimeError(f"Duplicate straal_exc entry for {code}")

        cls._REGISTRY[code] = cls


class card:
    class InvalidNumber(StraalError, code=10111):
        ...

    class InvalidExpiryYear(StraalError, code=10112):
        ...

    class InvalidExpiryMonth(StraalError, code=10113):
        ...

    class InvalidCVV(StraalError, code=10114):
        ...


class customer:
    class MissingCustomerEmail(StraalError, code=12001):
        ...

    class InvalidEmail(StraalError, code=12002):
        ...

    class EmailTooLong(StraalError, code=12003):
        ...

    class EmailTooShort(StraalError, code=12004):
        ...

    class ReferenceAlreadyExists(StraalError, code=12005):
        ...

    class ReferenceTooLong(StraalError, code=12006):
        ...
