import logging

import pytest

from pathlib import Path

from infrahub_sdk.client import InfrahubClient, InfrahubClientSync
from infrahub_sdk.protocols import CoreGenericRepository
from infrahub_sdk.spec.object import ObjectFile
from infrahub_sdk.testing.docker import TestInfrahubDockerClient
from infrahub_sdk.testing.repository import GitRepo
from infrahub_sdk.yaml import SchemaFile

logger = logging.getLogger(__name__)


class TestServiceCatalog(TestInfrahubDockerClient):

    @pytest.fixture(scope="class")
    def default_branch(self) -> str:
        return "main"

    @pytest.fixture(scope="class")
    def schema_definition(self, schema_dir: Path) -> list[SchemaFile]:
        return SchemaFile.load_from_disk(paths=[schema_dir])

    def test_schema_load(
        self, client_sync: InfrahubClientSync, schema_definition: list[SchemaFile], default_branch: str
    ):
        """
        Load the schema from the schema directory into the infrahub instance.
        """
        logger.info("Starting test: test_schema_load")

        client_sync.schema.load(schemas=[item.content for item in schema_definition])
        client_sync.schema.wait_until_converged(branch=default_branch)

    async def test_data_load(self, client: InfrahubClient, data_dir: Path, default_branch: str):
        """
        Load the data from the data directory into the infrahub instance.
        """
        logger.info("Starting test: test_data_load")

        await client.schema.all()
        object_files = sorted(ObjectFile.load_from_disk(paths=[data_dir]), key=lambda x: x.location)

        for idx, file in enumerate(object_files):
            file.validate_content()
            schema = await client.schema.get(kind=file.spec.kind, branch=default_branch)
            for item in file.spec.data:
                await file.spec.create_node(
                    client=client, position=[idx], schema=schema, data=item, branch=default_branch
                )

        countries = await client.all(kind="LocationCountry")
        assert len(countries) == 3

    async def test_add_repository(
        self, client: InfrahubClient, root_dir: Path, default_branch: str, remote_repos_dir: Path
    ) -> None:
        """
        Add the local directory as a repository in the infrahub instance in order to validate the import of the repository
        and have the generator operational in infrahub.
        """
        repo = GitRepo(name="devnet-live-2025", src_directory=root_dir, dst_directory=remote_repos_dir)
        await repo.add_to_infrahub(client=client)
        in_sync = await repo.wait_for_sync_to_complete(client=client)
        assert in_sync

        repos = await client.all(kind=CoreGenericRepository)
        assert repos
