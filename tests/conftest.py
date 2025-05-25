import json
from pathlib import Path
from typing import Any

import pytest

from infrahub_sdk import InfrahubClientSync, Config
from infrahub_sdk.ctl.repository import get_repository_config
from infrahub_sdk.schema.repository import InfrahubRepositoryConfig
from infrahub_sdk.yaml import SchemaFile

CURRENT_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def root_dir() -> Path:
    return Path(__file__).parent / ".."


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return CURRENT_DIR / "fixtures"


@pytest.fixture(scope="session")
def schema_dir(root_dir) -> Path:
    return root_dir / "schemas"


@pytest.fixture(scope="session")
def data_dir(root_dir) -> Path:
    return root_dir / "data"

