import logging
from figgy.figs import *
from figgy.fig_store import FigStore

log = logging.getLogger(__name__)

# Constants
ENV_LOCAL_RUN = 'LOCAL_RUN'


# All PS configurations are defined in our FigStore
class Figs(FigStore):
    # Twig = /app/your-service-name (this is required)
    TWIG: str = "/app/demo-service"

    # Custom Figs specific to my application (app figs)
    SECRET_ADMIRER = AppFig("secret-admirer")
    ADMIRED_PERSON = AppFig("admired-person")
    SQL_DB_NAME = AppFig("db-name", default="SecretAdmirerDB")

    # Figs shared by secret owners (shared figs)
    SQL_USER = SharedFig("replicated/sql/user")
    SQL_PASSWORD = SharedFig("replicated/sql/password")

    # Global figs used by many services that we need to use (replicated figs)
    SQL_HOSTNAME = ReplicatedFig(source="/shared/resources/dbs/fig-db/dns", name="replicated/sql/hostname")
    SQL_PORT = ReplicatedFig(source="/shared/resources/dbs/fig-db/port", name="replicated/sql/port")

    # Merged Connection URL (merged figs)
    SQL_CONNECTION_STRING = MergeFig(
        name="replicated/sql-connection",
        pattern=["mysql://", SQL_USER, ":", SQL_PASSWORD, "@", SQL_HOSTNAME, ":", SQL_PORT, "/", SQL_DB_NAME]
    )
