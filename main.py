import time

from constants import TARGET_MARKETS
from requests_clients import cg_client
from save_formats import JSONFormat, CSVFormat


def get_markets_for_asset(asset_id: str) -> list | None:
    """
    Возвращает список бирж на которых торгуется актив.
    Биржи binance, bybit, kucoin будут идти раньше в списке при наличии
    """
    asset_info = cg_client.get_coin_tickers_info(asset_id)
    if asset_info:
        try:
            data = asset_info.json()
            markets = [
                ticker["market"]["name"]
                for ticker in data["tickers"]
                if ticker.get("market") and ticker["market"].get("name")
            ]
            markets = list(set(markets))
            return sorted(markets, key=lambda ex: (ex not in TARGET_MARKETS, ex))
        except (AttributeError, ValueError, TypeError, KeyError):
            return None
    return None


def get_platforms_for_asset(asset_id: str) -> list[str] | None:
    """
    Возвращает список блокчейн-платформ, на которых доступен актив.
    Для нативных монет (BTC, ETH) возвращает название самой монеты.
    Для токенов возвращает список платформ (ethereum, binance-smart-chain, etc.)
    """
    response = cg_client.get_coin_info(asset_id)
    if not response:
        return None

    try:
        asset_data = response.json()
        platforms = []

        # Нативная монета (Bitcoin, Ethereum и т.д.)
        if asset_data.get("asset_platform_id") is None:
            if name := asset_data.get("name"):
                platforms.append(name)
            return platforms

        # Токен на разных платформах
        if asset_platforms := asset_data.get("platforms"):
            platforms.extend(asset_platforms.keys())

        return platforms if platforms else None

    except (AttributeError, ValueError, TypeError, KeyError):
        return None


if __name__ == "__main__":
    assets = []
    top_100_assets_by_volume = cg_client.get_coins_list(per_page=10).json()
    if not top_100_assets_by_volume:
        raise Exception("Can't get top 100 assets by volume")
    for asset in top_100_assets_by_volume:
        assets.append(
            {
                "name": asset["name"],
                "markets": get_markets_for_asset(asset["id"]),
                "platforms": get_platforms_for_asset(asset["id"]),
            }
        )
        time.sleep(4)
    JSONFormat().save(assets, "assets.json")
    CSVFormat().save(assets, "assets.csv")
