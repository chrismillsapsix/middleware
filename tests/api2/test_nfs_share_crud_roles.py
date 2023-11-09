import errno

import pytest

from middlewared.client import ClientException
from middlewared.test.integration.assets.nfs import nfs_share
from middlewared.test.integration.assets.pool import dataset
from middlewared.test.integration.assets.account import unprivileged_user_client


@pytest.fixture(scope="module")
def ds():
    with dataset("nfs_crud_test1") as ds:
        yield ds


@pytest.fixture(scope="module")
def share():
    with dataset("nfs_crud_test2") as ds:
        with nfs_share(ds) as share:
            yield share


@pytest.mark.parametrize("role", ["SHARING_READ", "SHARING_NFS_READ"])
def test_read_role_can_read(role):
    with unprivileged_user_client(roles=[role]) as c:
        c.call("sharing.nfs.query")


@pytest.mark.parametrize("role", ["SHARING_READ", "SHARING_NFS_READ"])
def test_read_role_cant_write(ds, share, role):
    with unprivileged_user_client(roles=[role]) as c:
        with pytest.raises(ClientException) as ve:
            c.call("sharing.nfs.create", {"path": f"/mnt/{ds}"})
        assert ve.value.errno == errno.EACCES

        with pytest.raises(ClientException) as ve:
            c.call("sharing.nfs.update", share["id"], {})
        assert ve.value.errno == errno.EACCES

        with pytest.raises(ClientException) as ve:
            c.call("sharing.nfs.delete", share["id"])
        assert ve.value.errno == errno.EACCES


@pytest.mark.parametrize("role", ["SHARING_WRITE", "SHARING_NFS_WRITE"])
def test_write_role_can_write(ds, role):
    with unprivileged_user_client(roles=[role]) as c:
        share = c.call("sharing.nfs.create", {"path": f"/mnt/{ds}"})

        c.call("sharing.nfs.update", share["id"], {})

        c.call("sharing.nfs.delete", share["id"])