# sqb-payment-reference-python-app

收钱吧支付参考应用（Python 版），按 `protocol -> adapter -> support -> bootstrap` 四层组织。

## 已完成模块

- Step 0：项目骨架（FastAPI、配置绑定、依赖注入）
- Step 1：签名模块（MD5 签名 + Authorization 组装）
- Step 2：状态判定（三层判定 + 终态识别）
- Step 3：终端激活（vendor 凭证签名）
- Step 4：终端签到（原子更新 terminal key）
- Step 5：B 扫 C 支付（支付 + 查询 + 轮询）
- Step 6：预下单 / 退款 / 撤单
- Step 7：异步回调（验签 + 幂等去重）
- Step 8：文档收尾（本文件）

## 目录结构

```text
app/
  protocol/
  adapter/
  support/
  service/
  bootstrap/routes/
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp app/settings.example.env .env
pytest -q
uvicorn app.main:app --reload
```

## API 端点

- `GET /health`
- `POST /terminal/activate`
- `POST /terminal/checkin`
- `POST /payment/pay`
- `POST /payment/precreate`
- `POST /payment/refund`
- `POST /payment/cancel`
- `POST /notify`

## 注意事项

- 当前 `SqbApiClient` 内置了演示级 stub 传输层；对接真实网关时请替换为 httpx 请求。
- 回调处理策略：先验签、再去重、最后处理；成功返回纯文本 `success`。
