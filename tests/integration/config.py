"""Shared configuration for integration tests.

Set the environment variables below (or edit the fallback values) before running.
"""

import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.environ.get("CREDERE_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL: str = os.environ.get("CREDERE_BASE_URL", "https://app.meucredere.com.br")
STORE_ID: int = int(os.environ.get("CREDERE_STORE_ID", "0"))  # fill in your store ID
CLIENT_CPF: str = os.environ.get("CLIENT_CPF", "0000000000")
SELLER_CPF: str = os.environ.get("SELLER_CPF", "0000000000")
