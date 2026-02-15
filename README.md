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

# Proposals
from credere import ProposalCreateRequest

proposal = client.proposals.create(ProposalCreateRequest(simulation_id="sim-uuid"))
proposal = client.proposals.get("proposal-uuid")
proposals = client.proposals.list()
activity = client.proposals.activity_log("proposal-uuid")

# Customers
from credere import CustomerCreateRequest

customer = client.customers.create(CustomerCreateRequest(cpf_cnpj="12345678900", name="João Silva"))
customer = client.customers.get(1)
customers = client.customers.list()
customer = client.customers.find(cpf_cnpj="12345678900")

# Stores
from credere import StoreCreateRequest

store = client.stores.create(StoreCreateRequest(name="Loja Centro", display_name="Centro", cnpj="12345678000100"))
stores = client.stores.list()
store = client.stores.activate(1)
store = client.stores.deactivate(1)

# Vehicle Models
models = client.vehicle_models.list()
model = client.vehicle_models.search(q="Civic")
prices = client.vehicle_models.prices()

# Stock
from credere import StockVehicleCreateRequest

vehicle = client.stock.create(StockVehicleCreateRequest(vehicle_model_id=1, store_id=1))
vehicles = client.stock.list()
vehicle = client.stock.update(1, StockVehicleCreateRequest(price_cents=5000000))
vehicle = client.stock.remove(1)

# Users
user = client.users.current()
users = client.users.proposals_filter_list()

# Utilities
domains = client.utilities.domains()
lead_domains = client.utilities.lead_domains()
banks = client.utilities.banks()
vehicle = client.utilities.vehicle_by_plate("ABC1D23")
vehicle = client.utilities.vehicle_by_chassis("9BWZZZ377VT004251")

# Bank Credentials
integrated_banks = client.bank_credentials.list(store_id=1)
client.bank_credentials.persist(store_id=1)

# Proposal Attempts
from credere import ProposalAttemptCreateRequest

attempt = client.proposal_attempts.create("proposal-uuid", ProposalAttemptCreateRequest())
attempts = client.proposal_attempts.list("proposal-uuid")
attempt = client.proposal_attempts.get("proposal-uuid", "attempt-uuid")
attempt = client.proposal_attempts.perform_action("proposal-uuid", "attempt-uuid", "approve")

# Plus Returns
from credere import PlusReturnRuleCreateRequest

rule = client.plus_returns.create(PlusReturnRuleCreateRequest())
rules = client.plus_returns.list()
rule = client.plus_returns.get(1)
rule = client.plus_returns.activate(1)
rule = client.plus_returns.deactivate(1)
client.plus_returns.delete(1)

client.close()
```

### Async client

```python
from credere import AsyncCredereClient

async with AsyncCredereClient(api_key="your-api-key", store_id=1) as client:
    leads = await client.leads.list()
    sims = await client.simulations.list()
    proposals = await client.proposals.list()
    customers = await client.customers.list()
    stores = await client.stores.list()
    models = await client.vehicle_models.list()
    vehicles = await client.stock.list()
    user = await client.users.current()
    domains = await client.utilities.domains()
    banks = await client.bank_credentials.list(store_id=1)
    attempts = await client.proposal_attempts.list("proposal-uuid")
    rules = await client.plus_returns.list()
```

## Features

- **Leads** — create, update, delete, list, get, and required_fields
- **Simulations** — create, list, and get
- **Proposals** — create, list, get, update, delete, ownership, and activity log
- **Customers** — create, update, list, get, and find
- **Stores** — create, list, activate, and deactivate
- **Users** — current user and proposals filter list
- **Vehicle Models** — list, search, and prices
- **Stock** — create, list, update, and remove
- **Utilities** — domains, lead domains, banks, vehicle by plate/chassis
- **Bank Credentials** — persist and list integrated banks
- **Proposal Attempts** — create, list, get, update, and perform action
- **Plus Returns** — create, list, get, update, delete, activate, and deactivate
- Sync and async clients (built on httpx)
- Pydantic models for request/response validation
- Error mapping (401, 404, timeouts, connection errors)
- Per-request `store_id` override

## License

Apache 2.0
