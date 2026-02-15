"""Credere SDK — Python client for the Credere credit simulation API."""

from credere.client import AsyncCredereClient, CredereClient
from credere.exceptions import (
    AuthenticationError,
    CredereAPIError,
    CredereConnectionError,
    CredereError,
    CredereTimeoutError,
    NotFoundError,
)
from credere.models.leads import (
    Address,
    DomainValue,
    Lead,
    LeadAddress,
    LeadCreateRequest,
    LeadRequiredFields,
)
from credere.models.simulations import (
    Bank,
    Simulation,
    SimulationCondition,
    SimulationConditionRequest,
    SimulationCreateRequest,
    SimulationVehicleRequest,
)
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
    "AsyncCredereClient",
    "AuthenticationError",
    "Bank",
    "CredereAPIError",
    "CredereClient",
    "CredereConnectionError",
    "CredereError",
    "CredereTimeoutError",
    "DomainValue",
    "Lead",
    "LeadAddress",
    "LeadCreateRequest",
    "LeadRequiredFields",
    "NotFoundError",
    "Simulation",
    "SimulationCondition",
    "SimulationConditionRequest",
    "SimulationCreateRequest",
    "SimulationVehicleRequest",
    "VehicleBrand",
    "VehicleFuel",
    "VehicleModel",
    "VehiclePrice",
    "VehiclePriceStore",
    "VehicleType",
]
