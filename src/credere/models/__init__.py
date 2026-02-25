"""Pydantic models for the Credere SDK."""

from credere.models.bank_credentials import IntegratedBank
from credere.models.customers import (
    Customer,
    CustomerAddress,
    CustomerAddressRequest,
    CustomerCreateRequest,
)
from credere.models.leads import (
    Address,
    DomainValue,
    Lead,
    LeadAddress,
    LeadCreateRequest,
    LeadRequiredFields,
)
from credere.models.plus_returns import PlusReturnRule, PlusReturnRuleCreateRequest
from credere.models.simulations import (
    Bank,
    Simulation,
    SimulationCondition,
    SimulationConditionRequest,
    SimulationCreateRequest,
    SimulationVehicleRequest,
)
from credere.models.stock import StockVehicle, StockVehicleCreateRequest
from credere.models.stores import Store, StoreCreateRequest
from credere.models.users import User, UserAccount, UserRole
from credere.models.utilities import Domain
from credere.models.vehicle_models import (
    VehicleBrand,
    VehicleFuel,
    VehicleModel,
    VehiclePrice,
    VehiclePriceStore,
    VehicleType,
)

__all__ = [
    "Address",
    "Bank",
    "Customer",
    "CustomerAddress",
    "CustomerAddressRequest",
    "CustomerCreateRequest",
    "Domain",
    "DomainValue",
    "IntegratedBank",
    "Lead",
    "LeadAddress",
    "LeadCreateRequest",
    "LeadRequiredFields",
    "PlusReturnRule",
    "PlusReturnRuleCreateRequest",
    "Simulation",
    "SimulationCondition",
    "SimulationConditionRequest",
    "SimulationCreateRequest",
    "SimulationVehicleRequest",
    "StockVehicle",
    "StockVehicleCreateRequest",
    "Store",
    "StoreCreateRequest",
    "User",
    "UserAccount",
    "UserRole",
    "VehicleBrand",
    "VehicleFuel",
    "VehicleModel",
    "VehiclePrice",
    "VehiclePriceStore",
    "VehicleType",
]
