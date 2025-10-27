# Asset Analyzer

## Описание

Проект получает топ-100 активов по объему торгов с CoinGecko, проверяет их доступность на биржах и определяет поддерживаемые блокчейн-сети.


## Установка
```bash
# Клонирование репозитория
git clone https://github.com/DoomsdayIS/EvercodeTest.git
cd coingecko-analyzer

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## Настройка

1. Создайте файл `.env` в корне проекта:
```bash
cp .env.example .env
```

2. Введите ваш API ключ от CoinGecko:
```env
COINGECKO_API_KEY=your_api_key_here
```


## Использование
```bash
python main.py
```

## Формат выходных данных

### JSON
Пример: [`assets.json`](./assets.json)

### CSV
Пример: [`assets.csv`](./assets.csv)

## Приоритетность добавления полученных активов

Можно реализовать приорететность активов по следующим параметрам:

- Наличие торгов на целевых биржах (Binance, Bybit, KuCoin)
- Объем торгов
- Доступность на популярных сетях (Ethereum, BNB Chain, Solana)
- Дата выхода на рынок (можно получить по каждому конкретному активу через api CoinGecko)

```python
priority_score = (
    target_exchanges_count * 10 +  # 0-30 баллов
    volume_rank_bonus +             # 0-10 баллов
    platforms_count * 2 +           # 0-20 баллов
    recency_bonus                   # 0-5 баллов
)
```

