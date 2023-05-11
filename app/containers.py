"""



@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""


from dependency_injector import containers, providers

from .database import Database
from .external_services import CurrencyExchangeRatesAPIClient as Service
from .my_services import MyDatabaseService as DBService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yaml"])

    external_service = providers.Factory(
        Service,
        timeout=config.exchange_api.timeout,
    )

    db = providers.Singleton(
        Database,
        db_url=config.db.url,
    )

    db_service = providers.Factory(
        DBService,
        session_factory=db.provided.provided_session,
    )
