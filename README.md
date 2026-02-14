# credere-sdk

Python SDK for the Credere credit simulation API.

## Installation

```bash
pip install credere-sdk
```

## Usage

### Sync client

```python
from credere import CredereClient

client = CredereClient(api_key="your-api-key", store_id=1)

# Leads
from credere import LeadCreateRequest

lead = client.leads.create(LeadCreateRequest(cpf_cnpj="12345678900", name="João Silva"))
lead = client.leads.get("12345678900")
leads = client.leads.list()
lead = client.leads.update("12345678900", LeadCreateRequest(name="João Atualizado"))
client.leads.delete("12345678900")
fields = client.leads.required_fields("12345678900")

# Simulations
from credere import SimulationCreateRequest, SimulationConditionRequest, SimulationVehicleRequest

sim = client.simulations.create(SimulationCreateRequest(
    assets_value=5000000,
    conditions=[SimulationConditionRequest(down_payment=1000000, financed_amount=4000000, installments=48)],
    retrieve_lead={"cpf_cnpj": "12345678900"},
    seller_cpf="98765432100",
    vehicle=SimulationVehicleRequest(
        asset_value=5000000,
        licensing_uf="SP",
        manufacture_year=2024,
        model_year=2024,
        vehicle_molicar_code="MOL123",
        zero_km=True,
    ),
))
sim = client.simulations.get("simulation-uuid")
sims = client.simulations.list()

client.close()
```

### Async client

```python
from credere import AsyncCredereClient

async with AsyncCredereClient(api_key="your-api-key", store_id=1) as client:
    leads = await client.leads.list()
    sims = await client.simulations.list()
```

## Features

- **Leads** — create, update, delete, list, get, and required_fields
- **Simulations** — create, list, and get
- Sync and async clients (built on httpx)
- Pydantic models for request/response validation
- Error mapping (401, 404, timeouts, connection errors)
- Per-request `store_id` override

## License

Apache 2.0
