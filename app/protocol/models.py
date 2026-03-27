from pydantic import BaseModel, Field


class ActivateRequest(BaseModel):
    terminal_sn: str
    terminal_name: str


class ActivateResponse(BaseModel):
    terminal_sn: str
    terminal_key: str
    status: str = "ACTIVATED"


class CheckinRequest(BaseModel):
    terminal_sn: str


class CheckinResponse(BaseModel):
    terminal_sn: str
    terminal_key: str


class PayRequest(BaseModel):
    terminal_sn: str
    client_sn: str
    total_amount: int = Field(gt=0)
    auth_code: str
    subject: str


class PrecreateRequest(BaseModel):
    terminal_sn: str
    client_sn: str
    total_amount: int = Field(gt=0)
    subject: str


class OrderQueryRequest(BaseModel):
    terminal_sn: str
    client_sn: str


class RefundRequest(BaseModel):
    terminal_sn: str
    client_sn: str
    refund_amount: int = Field(gt=0)
    refund_request_no: str


class CancelRequest(BaseModel):
    terminal_sn: str
    client_sn: str


class ApiResult(BaseModel):
    result_code: str = "200"
    error_message: str | None = None
    biz_response: dict = Field(default_factory=dict)
