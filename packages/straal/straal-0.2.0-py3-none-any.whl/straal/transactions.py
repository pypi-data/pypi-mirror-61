import datetime
import enum
from dataclasses import dataclass, field
from typing import Optional

from straal.base import ApiObject


class InitiatedBy(enum.Enum):
    MERCHANT = "merchant"
    CUSTOMER = "customer"


@dataclass
class CardTransaction(ApiObject):
    RESOURCE_CREATE_URI = "/v1/cards/{card_id}/transactions"
    RESOURCE_DETAIL_URI = "/v1/transactions/{idx}"
    RESOURCE_LIST_URI = "/v1/transactions?method__eq=card"
    # API PRIMITIVE FIELDS
    id: str
    amount: int
    currency: str
    authorized: bool
    captured: bool
    refunded: bool
    voided: bool
    method: str
    reference: str
    # COMPOUND FIELDS
    captures: list = field(repr=False)
    refunds: list = field(repr=False)
    voids: list = field(repr=False)
    attempts: list = field(repr=False)
    created_at: datetime.datetime = field(repr=False)
    extra_data: dict = field(repr=False)
    order_reference: Optional[str] = field(default=None, repr=False)
    card: Optional[dict] = field(default=None, repr=False)
    chargeback: Optional[dict] = field(default=None, repr=False)
    decline_reason: Optional[dict] = field(default=None, repr=False)
    errors: Optional[list] = field(default=None, repr=False)

    def __post_init__(self):
        self.created_at = datetime.datetime.utcfromtimestamp(self.created_at)

    @classmethod
    def create(
        cls,
        card_id: str,
        amount: int,
        currency: str,
        reference: str,
        initiated_by: InitiatedBy,
    ) -> "CardTransaction":
        return super().create(
            card_id=card_id,
            amount=amount,
            currency=currency,
            reference=reference,
            initiated_by=initiated_by.value,
        )

    @classmethod
    def get(cls, id: str) -> "CardTransaction":
        return super().get(idx=id)

    @classmethod
    def list(cls) -> "CardTransaction":
        return super().list()
