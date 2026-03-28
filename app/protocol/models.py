from pydantic import BaseModel, Field, field_validator, model_validator


def _validate_positive_decimal_string(value: str) -> str:
    if not value.isdigit() or int(value) <= 0:
        raise ValueError("must be a positive integer string")
    return value


class ActivateRequest(BaseModel):
    app_id: str
    code: str
    device_id: str


class ActivateResponse(BaseModel):
    terminal_sn: str
    terminal_key: str
    status: str = "ACTIVATED"


class CheckinRequest(BaseModel):
    terminal_sn: str
    device_id: str


class CheckinResponse(BaseModel):
    terminal_sn: str
    terminal_key: str


class PayRequest(BaseModel):
    terminal_sn: str
    client_sn: str
    total_amount: str = Field(min_length=1)
    dynamic_id: str
    operator: str
    subject: str

    _validate_total_amount = field_validator("total_amount")(_validate_positive_decimal_string)


class PrecreateRequest(BaseModel):
    terminal_sn: str
    client_sn: str
    total_amount: str = Field(min_length=1)
    operator: str
    payway: str
    subject: str

    _validate_total_amount = field_validator("total_amount")(_validate_positive_decimal_string)


class OrderQueryRequest(BaseModel):
    terminal_sn: str
    client_sn: str | None = None
    sn: str | None = None

    @model_validator(mode="after")
    def validate_query_key(self) -> "OrderQueryRequest":
        if not (self.client_sn or self.sn):
            raise ValueError("either client_sn or sn is required")
        return self


class RefundRequest(BaseModel):
    terminal_sn: str
    refund_amount: str = Field(min_length=1)
    operator: str
    client_sn: str | None = None
    sn: str | None = None
    refund_request_no: str

    _validate_refund_amount = field_validator("refund_amount")(_validate_positive_decimal_string)

    @model_validator(mode="after")
    def validate_refund_target(self) -> "RefundRequest":
        if not (self.client_sn or self.sn):
            raise ValueError("either client_sn or sn is required")
        return self


class CancelRequest(BaseModel):
    terminal_sn: str
    client_sn: str | None = None
    sn: str | None = None

    @model_validator(mode="after")
    def validate_cancel_target(self) -> "CancelRequest":
        if not (self.client_sn or self.sn):
            raise ValueError("either client_sn or sn is required")
        return self


class ApiResult(BaseModel):
    result_code: str = "200"
    error_message: str | None = None
    biz_response: dict = Field(default_factory=dict)
