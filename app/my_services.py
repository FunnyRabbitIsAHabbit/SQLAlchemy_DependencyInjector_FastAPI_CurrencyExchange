"""



@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from .models import Currency, CurrencyModel


class MyDatabaseService:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def read_all(self) -> Iterator[Currency] | list[Currency]:
        try:

            with self.session_factory() as session:
                return session.query(Currency).all()

        except OperationalError:
            return [Currency()]

    def read_single(self, currency_code: str, target_currency_code: str) -> Currency:
        with self.session_factory() as session:
            row: Currency = session.query(Currency).filter(
                Currency.base == currency_code).filter(Currency.target_code == target_currency_code).first()

            return row

    def update(self, data: CurrencyModel) -> bool:
        with self.session_factory() as session:
            cur = session.query(Currency).filter(Currency.base == data.base).filter(
                Currency.target_code == data.target_code).first()

            if cur:
                cur.rate = data.rate

            else:
                session.add(Currency(**data.dict()))

            session.commit()

            return True


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class CurrencyNotFoundError(NotFoundError):
    entity_name: str = "Currency"
