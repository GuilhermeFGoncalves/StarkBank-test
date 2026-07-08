# StarkBank-test

Integração Stark Bank (Sandbox): emite Invoices periodicamente e, ao receber o
webhook de crédito, transfere o valor líquido (amount - fee) para a conta alvo.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha STARKBANK_PROJECT_ID e STARKBANK_PRIVATE_KEY
export $(cat .env | xargs)
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Expor o webhook (sandbox precisa de URL pública)

```bash
ngrok http 8000
```

Registre a URL `https://<subdominio>.ngrok.app/webhook/stark/` como Webhook no
painel do Sandbox (subscription `invoice`).

## Agendar a emissão de invoices (cron local, 8x em 24h a cada 3h)

```bash
crontab -e
```

Adicione (ajuste os caminhos):

```
0 */3 * * * cd /caminho/para/StarkBank-test && /caminho/para/.venv/bin/python manage.py issue_invoices >> /tmp/issue_invoices.log 2>&1
```

Isso roda o comando em `00:00, 03:00, 06:00, ...`, cobrindo 24h com invoices
de 8 a 12 clientes aleatórios a cada execução.
