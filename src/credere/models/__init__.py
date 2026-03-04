"""Pydantic models for the Credere SDK."""

from credere.models.bank_credentials import Bank, IntegratedBank
from credere.models.customers import (
    Accountant,
    BankReference,
    BankValidations,
    CustomerData,
    CustomerResponse,
    Domain,
    Email,
    JobReference,
    PersonalReference,
)
from credere.models.customers import (
    Address as CustomerAddress,
)
from credere.models.customers import (
    Phone as CustomerPhone,
)
from credere.models.leads import (
    Address as LeadAddress,
)
from credere.models.leads import (
    DomainValue,
    LeadData,
    LeadRequiredFields,
    LeadResponse,
)
from credere.models.plus_returns import PlusReturnRule, PlusReturnRuleCreateRequest
from credere.models.proposal_attempts import (
    ProposalAttemptData,
    ProposalAttemptRequest,
    ProposalAttemptResponse,
)
from credere.models.proposals import (
    ProposalAttempt,
    ProposalData,
    ProposalResponse,
)
from credere.models.simulations import (
    Condition,
    ProductsOptions,
    RetrieveLead,
    SimulationData,
    SimulationResponse,
    Vehicle,
)
from credere.models.stock import StockVehicle, StockVehicleCreateRequest
from credere.models.stores import Store, StoreCreateRequest
from credere.models.users import User, UserAccount, UserRole
from credere.models.vehicle_models import (
    Fuel,
    VehicleBrand,
    VehicleModel,
    VehicleModelSummary,
    VehiclePrice,
    VehicleType,
)

__all__ = [
    "Accountant",
    "Bank",
    "BankReference",
    "BankValidations",
    "Condition",
    "CustomerAddress",
    "CustomerData",
    "CustomerPhone",
    "CustomerResponse",
    "Domain",
    "DomainValue",
    "Email",
    "Fuel",
    "IntegratedBank",
    "JobReference",
    "LeadAddress",
    "LeadData",
    "LeadRequiredFields",
    "LeadResponse",
    "PersonalReference",
    "PlusReturnRule",
    "PlusReturnRuleCreateRequest",
    "ProductsOptions",
    "ProposalAttempt",
    "ProposalAttemptData",
    "ProposalAttemptRequest",
    "ProposalAttemptResponse",
    "ProposalData",
    "ProposalResponse",
    "RetrieveLead",
    "SimulationData",
    "SimulationResponse",
    "StockVehicle",
    "StockVehicleCreateRequest",
    "Store",
    "StoreCreateRequest",
    "User",
    "UserAccount",
    "UserRole",
    "Vehicle",
    "VehicleBrand",
    "VehicleModel",
    "VehicleModelSummary",
    "VehiclePrice",
    "VehicleType",
]
