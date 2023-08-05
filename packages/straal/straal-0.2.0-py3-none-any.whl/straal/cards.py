import datetime
import enum
from dataclasses import dataclass, field

from straal.base import ApiObject


class CardBrand(enum.Enum):
    AMEX = "amex"
    MAESTRO = "maestro"
    MASTERCARD = "mastercard"
    VISA = "visa"
    VISA_ELECTRON = "visa_electron"
    UNKNOWN = "unknown"


class CardState(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


@dataclass
class Card(ApiObject):
    RESOURCE_CREATE_URI = "/v1/customers/{customer_id}/cards"
    RESOURCE_DETAIL_URI = "/v1/cards/{idx}"
    RESOURCE_LIST_URI = "/v1/cards"
    # API PRIMITIVE FIELDS
    id: str
    name: str
    num_bin: str
    num_last_4: str
    expiry_month: int
    expiry_year: int
    origin_ipaddr: str
    # COMPOUND FIELDS
    brand: CardBrand = field(repr=False)
    state: CardState = field(repr=False)
    created_at: datetime.datetime = field(repr=False)
    customer: dict = field(repr=False)
    extra_data: dict = field(repr=False)
    straal_custom_data: dict = field(repr=False)
    state_flags: list = field(repr=False)
    transactions: list = field(default=None, repr=False)
    # VIRTUAL FIELDS
    is_active: bool = None

    def __post_init__(self):
        self.brand = CardBrand(self.brand)
        self.state = CardState(self.state)
        self.is_active = self.state == CardState.ACTIVE
        self.created_at = datetime.datetime.utcfromtimestamp(self.created_at)

    @classmethod
    def create(
        cls,
        customer_id: str,
        name: str,
        number: str,
        cvv: str,
        expiry_year: int,
        expiry_month: int,
        origin_ipaddr: str,
    ) -> "Card":
        return super().create(
            customer_id=customer_id,
            name=name,
            number=number,
            cvv=cvv,
            expiry_year=expiry_year,
            expiry_month=expiry_month,
            origin_ipaddr=origin_ipaddr,
        )

    @classmethod
    def get(cls, id: str) -> "Card":
        return super().get(idx=id)

    @classmethod
    def list(cls) -> "Card":
        return super().list()
