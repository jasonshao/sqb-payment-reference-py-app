from enum import StrEnum


class OrderStatus(StrEnum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELED = "CANCELED"
    REFUNDED = "REFUNDED"
    PARTIAL_REFUNDED = "PARTIAL_REFUNDED"
    USERPAYING = "USERPAYING"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

    @property
    def is_final(self) -> bool:
        return self in {
            self.PAID,
            self.CANCELED,
            self.REFUNDED,
            self.PARTIAL_REFUNDED,
            self.FAILED,
        }
