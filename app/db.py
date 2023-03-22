import os
import pathlib
from cassandra.cluster import DEFAULT_MAX_CONNECTIONS_PER_LOCAL_HOST 



DEFAULT_MAX_CONNECTIONS_PER_LOCAL_HOST = 3 

# cass_cluster_set_protocol_version(cluster, CASS_PROTOCOL_VERSION_V4)

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection
from .config import get_settings

settings = get_settings()

ASTRA_DB_CLIENT_ID = settings.db_client_id
ASTRA_DB_CLIENT_SECRET = settings.db_client_secret

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / "bundle" / 'connect.zip')

def get_cluster():
    cloud_config= {
        'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider,protocol_version=4)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session
