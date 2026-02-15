"""Resource classes for the Credere SDK."""

from credere.resources.leads import AsyncLeads, Leads
from credere.resources.proposal_attempts import AsyncProposalAttempts, ProposalAttempts
from credere.resources.proposals import AsyncProposals, Proposals
from credere.resources.simulations import AsyncSimulations, Simulations
from credere.resources.stores import AsyncStores, Stores
from credere.resources.users import AsyncUsers, Users
from credere.resources.utilities import AsyncUtilities, Utilities
from credere.resources.vehicle_models import AsyncVehicleModels, VehicleModels

__all__ = [
    "AsyncLeads",
    "AsyncProposalAttempts",
    "AsyncProposals",
    "AsyncSimulations",
    "AsyncStores",
    "AsyncUsers",
    "AsyncUtilities",
    "AsyncVehicleModels",
    "Leads",
    "ProposalAttempts",
    "Proposals",
    "Simulations",
    "Stores",
    "Users",
    "Utilities",
    "VehicleModels",
]
