"""
API Endpoints

GET /all
GET /convert?base=USD&symbol=EUR&amount=10



@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""

from decimal import Decimal, getcontext

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status

from .containers import Container
from .external_services import CurrencyExchangeRatesAPIClient as Service
from .models import DataForExternalAPIOut, Currency, DataForConversionFromExternal, CurrencyModel, \
    InfoDataForExternalAPIIn
from .my_services import MyDatabaseService as DBService

getcontext().prec = 10

router = APIRouter()


@router.get('/all', response_model=DataForExternalAPIOut)
@inject
async def index_all(db_service: DBService = Depends(Provide[Container.db_service])) -> Response | DataForExternalAPIOut:
    try:
        data: list[Currency] = db_service.read_all()
        formatted_data = [CurrencyModel.parse_obj({col.name: getattr(obj, col.name)
                                                   for col in Currency.__table__.columns})
                          for obj in data]

        out_result: DataForExternalAPIOut = DataForExternalAPIOut.parse_obj({"response": formatted_data})

        return out_result

    except Exception as error:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"{error}")


@router.get('/convert', response_model=CurrencyModel)
@inject
async def index_single(base: str, symbol: str, amount: Decimal = None,
                       external_service: Service = Depends(Provide[Container.external_service]),
                       db_service: DBService = Depends(
                           Provide[Container.db_service])) -> Response | CurrencyModel:
    try:

        # Get from external
        api_result: dict = await external_service.get_conversion_rate(base=base, symbol=symbol)
        result: DataForConversionFromExternal = DataForConversionFromExternal.parse_obj(api_result)

        out_result: CurrencyModel = CurrencyModel.parse_obj(result)
        out_result.target_code = symbol
        out_result.rate = result.rates.get(symbol)

        # Update DB
        _currency_names: dict = await external_service.get_supported_symbols()
        currency_names: InfoDataForExternalAPIIn = InfoDataForExternalAPIIn.parse_obj(_currency_names)
        currency_name: str = currency_names.symbols.get(base).description
        out_result.description = currency_name

        db_service.update(out_result)

        # Read from DB as per technical request ------
        # Personally, I don't think that's optimal ---
        data = db_service.read_single(base, symbol)
        formatted_data = CurrencyModel.parse_obj({col.name: getattr(data, col.name)
                                                  for col in Currency.__table__.columns})
        # --------------------------------------------

        formatted_data.rate *= amount

        return formatted_data

    except Exception as error:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"{error}")
