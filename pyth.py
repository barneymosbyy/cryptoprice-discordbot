import asyncio
import requests
import datetime
from pytz import timezone
import pythclient.exceptions
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, PYTHNET_HTTP_ENDPOINT, PYTHNET_WS_ENDPOINT

PYTH_EVM_PRICE_ID = "0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43"
SOLANA_PRICE_ID = "nrYkQQQur7z8rYTST3G9GqATviK5SxTDkrqd21MW6Ue"


async def get_price():
    # pythnet SOL/USD price account key (available on pyth.network website)
    account_key = SolanaPublicKey(SOLANA_PRICE_ID)
    solana_client = SolanaClient(endpoint=PYTHNET_HTTP_ENDPOINT, ws_endpoint=PYTHNET_WS_ENDPOINT)
    price: PythPriceAccount = PythPriceAccount(account_key, solana_client)

    try:
        await price.update()
        price_status = price.aggregate_price_status
        if price_status == PythPriceStatus.TRADING:
            solprice = price.aggregate_price
            return solprice
        else:
            print("Price is not valid now. Status is", price_status)
            await asyncio.sleep(30)
            await solana_client.close()
            return await get_price()
    except pythclient.exceptions.SolanaException:
        print("pythclient.exceptions.SolanaException. Waiting 30 seconds and trying again.")
        await asyncio.sleep(30)
        await solana_client.close()
        return await get_price()
    except RuntimeError as e:
        print("RuntimeError:", e)
        await asyncio.sleep(30)
        await solana_client.close()
        return await get_price()  # Recreate the session and retry the request
    except Exception as e:
        print("Error:", e)
        await asyncio.sleep(30)
        await solana_client.close()
        return await get_price()
    finally:
        await solana_client.close()


async def get_price_change():
    cet_timezone = timezone('UTC')
    current_datetime = datetime.datetime.now(cet_timezone)
    daily_close = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    daily_close_unix = int(daily_close.timestamp())

    while True:
        price_data = requests.get(f"https://hermes.pyth.network/api/get_price_feed?id={PYTH_EVM_PRICE_ID}&publish_time={daily_close_unix}")

        if price_data.status_code == 200:
            price_data_json = price_data.json()
            daily_close_price = int(price_data_json["price"]["price"]) / 1e8
            return daily_close_price
        else:
            print(f"Request failed with status code: {price_data.status_code}")
            await asyncio.sleep(5)
