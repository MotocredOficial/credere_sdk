"""Shared configuration for integration tests.

Set the environment variables below (or edit the fallback values) before running.
"""

import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.environ.get("API_KEY", "YOUR_API_KEY_HERE")
BASE_URL: str = os.environ.get("BASE_URL", "https://app.meucredere.com.br")
STORE_ID: int = int(os.environ.get("STORE_ID", "0"))
EXISTING_CPF: str = os.environ.get("EXISTING_CPF", "0000000000")
SELLER_CPF: str = os.environ.get("SELLER_CPF", "0000000000")
