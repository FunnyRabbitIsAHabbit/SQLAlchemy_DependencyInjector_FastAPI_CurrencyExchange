"""



@App: API for currency exchange external API
@Version: 1.0.0
@Version-description: Non-public
@Developer: Stan Ermokhin
@GitHub: FunnyRabbitIsAHabbit
"""


from aiohttp import ClientSession, ClientTimeout, TCPConnector


class CurrencyExchangeRatesAPIClient:
    API_BASE_URL = "https://api.exchangerate.host"

    def __init__(self, timeout):
        self.timeout: ClientTimeout = ClientTimeout(timeout)

    async def get_latest_data(self):

        async with ClientSession(connector=TCPConnector(verify_ssl=False), timeout=self.timeout) as session:
            url = f"{self.API_BASE_URL}/latest"

            async with session.get(url) as result:
                if result.status != 200:
                    result.raise_for_status()

                return await result.json()

    async def get_conversion_rate(self, base: str, symbol: str):

        async with ClientSession(connector=TCPConnector(verify_ssl=False), timeout=self.timeout) as session:
            url = f"{self.API_BASE_URL}/latest"
            parameters = {
                "base": base,
                "symbols": symbol,
            }

            async with session.get(url, params=parameters) as result:
                if result.status != 200:
                    result.raise_for_status()

                return await result.json()

    async def get_supported_symbols(self):

        async with ClientSession(connector=TCPConnector(verify_ssl=False), timeout=self.timeout) as session:
            url = f"{self.API_BASE_URL}/symbols"

            async with session.get(url) as result:
                if result.status != 200:
                    result.raise_for_status()

                return await result.json()
