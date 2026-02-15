"""Resource classes for the Credere SDK."""

from credere.resources.bank_credentials import AsyncBankCredentials, BankCredentials
from credere.resources.leads import AsyncLeads, Leads
from credere.resources.plus_returns import AsyncPlusReturns, PlusReturns
from credere.resources.proposal_attempts import AsyncProposalAttempts, ProposalAttempts
from credere.resources.proposals import AsyncProposals, Proposals
from credere.resources.simulations import AsyncSimulations, Simulations
from credere.resources.stock import AsyncStock, Stock
from credere.resources.stores import AsyncStores, Stores
from credere.resources.users import AsyncUsers, Users
from credere.resources.utilities import AsyncUtilities, Utilities
from credere.resources.vehicle_models import AsyncVehicleModels, VehicleModels

__all__ = [
    "AsyncBankCredentials",
    "AsyncLeads",
    "AsyncPlusReturns",
    "AsyncProposalAttempts",
    "AsyncProposals",
    "AsyncSimulations",
    "AsyncStock",
    "AsyncStores",
    "AsyncUsers",
    "AsyncUtilities",
    "AsyncVehicleModels",
    "BankCredentials",
    "Leads",
    "PlusReturns",
    "ProposalAttempts",
    "Proposals",
    "Simulations",
    "Stock",
    "Stores",
    "Users",
    "Utilities",
    "VehicleModels",
]
