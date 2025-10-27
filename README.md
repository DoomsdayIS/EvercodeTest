# Asset Analyzer

## Описание

Проект получает топ-100 активов по объему торгов с CoinGecko, проверяет их доступность на биржах и определяет поддерживаемые блокчейн-сети.


## Установка
```bash
# Клонирование репозитория
git clone https://github.com/your-username/coingecko-analyzer.git
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

