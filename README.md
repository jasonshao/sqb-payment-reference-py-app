# sqb-payment-reference-python-app

收钱吧支付参考应用（Python / FastAPI）。这个项目更适合作为分层设计、签名、终端激活、支付轮询和回调验签的参考实现，而不是可直接投产的完整支付网关。

## 这个项目适合谁

- 想了解一个支付服务在 Python 中如何按 `protocol -> adapter -> support -> service -> bootstrap` 分层组织
- 想快速跑通终端激活、签到、支付、退款、撤单、异步回调的接口骨架
- 想基于现有代码替换 stub 传输层，继续对接真实收钱吧接口

## 当前能力边界

- 已包含：FastAPI 应用骨架、配置绑定、签名、状态判定、终端激活/签到、支付/查询轮询、退款/撤单、异步回调验签和幂等去重
- 未包含：真实网关 HTTP 调用、生产级鉴权治理、持久化存储、监控告警、完整错误码映射
- 重要说明：当前 `SqbApiClient` 使用的是演示级 stub 传输层，对接真实网关时需要替换为实际的 `httpx` 请求实现

## 前置要求

- Python `3.11+`
- 建议使用虚拟环境
- 建议先升级 `pip`，避免旧版本对 `pyproject.toml` 安装支持不完整

## 快速开始

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp app/settings.example.env .env
uvicorn app.main:app --reload
```

服务启动后可访问：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 配置说明

运行时配置通过 `.env` 加载，示例文件见 [app/settings.example.env](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/app/settings.example.env)。

| 变量名 | 是否必需 | 说明 | 示例 |
| --- | --- | --- | --- |
| `APP_NAME` | 否 | 应用名称 | `SQB Payment Reference Python App` |
| `APP_ENV` | 否 | 运行环境标记 | `dev` |
| `APP_DEBUG` | 否 | 是否开启调试 | `false` |
| `SQB_BASE_URL` | 否 | 收钱吧基础地址 | `https://api.shouqianba.com` |
| `SQB_VENDOR_SN` | 建议填写 | 服务商编号 | `your_vendor_sn` |
| `SQB_VENDOR_KEY` | 建议填写 | 服务商签名密钥 | `your_vendor_key` |
| `SQB_ACCESS_TOKEN` | 建议填写 | 平台访问令牌 | `your_access_token` |

说明：

- 目前仓库里的适配器包含 stub 行为，即使不接真实网关也可以本地联调部分流程
- 如果你要替换成真实接口，`SQB_VENDOR_SN`、`SQB_VENDOR_KEY`、`SQB_ACCESS_TOKEN` 应视为必填

## 运行测试

```bash
source .venv/bin/activate
pytest -q
```

已配置的 pytest 信息：

- 测试目录：`tests/`
- 导入根路径：项目根目录
- 当前项目语法和类型目标版本为 Python 3.11

常见问题：

- 如果你使用的是 Python 3.9 或 3.10，测试可能会在收集阶段失败
- 原因包括 `str | None` 和 `enum.StrEnum` 等 Python 3.11 运行时能力差异

## 项目结构

```text
app/
  protocol/            # 协议对象、状态定义、请求响应模型
  adapter/             # 面向收钱吧的适配层
  support/             # 签名、验签、轮询、去重等支撑能力
  service/             # 支付流程与回调处理编排
  bootstrap/routes/    # FastAPI 路由入口
tests/                 # 接口与支撑逻辑测试
```

## API 概览

- `GET /health`
- `POST /terminal/activate`
- `POST /terminal/checkin`
- `POST /payment/pay`
- `POST /payment/precreate`
- `POST /payment/refund`
- `POST /payment/cancel`
- `POST /notify`

## 最小调用示例

### 1. 健康检查

```bash
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{"status":"ok"}
```

### 2. 激活终端

```bash
curl -X POST http://127.0.0.1:8000/terminal/activate \
  -H 'Content-Type: application/json' \
  -d '{
    "terminal_sn": "T1",
    "terminal_name": "POS-1"
  }'
```

预期返回：

```json
{
  "terminal_sn": "T1",
  "terminal_key": "key-T1"
}
```

### 3. 终端签到

签到前请先完成激活，否则会返回 `404 terminal not activated`。

```bash
curl -X POST http://127.0.0.1:8000/terminal/checkin \
  -H 'Content-Type: application/json' \
  -d '{
    "terminal_sn": "T1"
  }'
```

### 4. 发起支付

```bash
curl -X POST http://127.0.0.1:8000/payment/pay \
  -H 'Content-Type: application/json' \
  -d '{
    "terminal_sn": "T1",
    "client_sn": "ORDER1",
    "total_amount": 100,
    "auth_code": "28937492374923",
    "subject": "coffee"
  }'
```

返回结构示例：

```json
{
  "status": "USERPAYING",
  "final": false,
  "success": false
}
```

### 5. 接收异步回调

`/notify` 需要请求头 `X-SQB-Signature`。成功时返回纯文本 `success`。

示例请求体：

```json
{"event":"payment","terminal_sn":"NT1","client_sn":"C1","status":"PAID","amount":100}
```

说明：

- 签名值需要使用对应终端密钥计算
- 当前测试里，激活终端 `NT1` 后默认可得到 `terminal_key = key-NT1`
- 回调处理顺序为：先验签、再去重、最后执行业务处理

## 开发说明

- 本项目按分层结构组织，适合作为继续扩展的起点
- 如果你要接入真实网关，优先从 [app/adapter/base_client.py](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/app/adapter/base_client.py) 和 [app/adapter/](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/app/adapter) 开始替换 stub 调用
- 如果你要调整环境变量绑定，可查看 [app/core/config.py](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/app/core/config.py)
- 如果你要看接口行为，可优先阅读 [tests/test_health.py](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/tests/test_health.py), [tests/test_payment_endpoints.py](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/tests/test_payment_endpoints.py), [tests/test_terminal_and_notify.py](/Users/suwenjuan/Ai/sqb-payment-reference-py-app/tests/test_terminal_and_notify.py)

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
