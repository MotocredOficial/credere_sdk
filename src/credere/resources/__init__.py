"""Resource classes for the Credere SDK."""

from credere.resources.leads import AsyncLeads, Leads
from credere.resources.proposals import AsyncProposals, Proposals
from credere.resources.simulations import AsyncSimulations, Simulations
from credere.resources.stores import AsyncStores, Stores
from credere.resources.vehicle_models import AsyncVehicleModels, VehicleModels

__all__ = [
    "AsyncLeads",
    "AsyncProposals",
    "AsyncSimulations",
    "AsyncStores",
    "AsyncVehicleModels",
    "Leads",
    "Proposals",
    "Simulations",
    "Stores",
    "VehicleModels",
]
