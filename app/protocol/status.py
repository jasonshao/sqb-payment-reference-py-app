from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    PAY_CANCELED = "PAY_CANCELED"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

    @property
    def is_final(self) -> bool:
        return self in {self.PAID, self.PAY_CANCELED, self.REFUNDED, self.FAILED}
