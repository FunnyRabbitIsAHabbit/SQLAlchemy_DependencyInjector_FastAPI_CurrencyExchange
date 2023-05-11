"""



@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""


from decimal import Decimal, getcontext

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, DECIMAL

from .database import Base

getcontext().prec = 10


class CurrencyModel(BaseModel):
    description: str | None
    base: str
    date: str | None

    # Rates of exchange
    target_code: str | None
    rate: Decimal | None = Field(decimal_places=10)


class Currency(Base):
    __tablename__ = "currency"

    # Currencies general info
    id: int = Column(Integer, primary_key=True)
    description: str = Column(String(255), nullable=True)
    base: str = Column(String(3), nullable=False)
    date: str = Column(String(10), nullable=True)

    # Rates of exchange
    target_code: str = Column(String(3), nullable=True)
    rate: Decimal = Column(DECIMAL, nullable=True)

    def __repr__(self):
        return f"<Currency(id={self.id}, " \
               f"code={self.code}"


class DataForExternalAPIIn(BaseModel):
    motd: dict[str, str]
    success: bool
    base: str
    date: str
    rates: CurrencyModel


class InfoOnCurrency(BaseModel):
    description: str
    code: str


class InfoDataForExternalAPIIn(BaseModel):
    motd: dict[str, str]
    success: bool
    symbols: dict[str, InfoOnCurrency]


class DataForConversionFromExternal(BaseModel):
    rates: dict[str, Decimal]
    date: str
    base: str


class DataForExternalAPIOut(BaseModel):
    response: list[CurrencyModel]
