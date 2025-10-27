import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any


class SaveFormat(ABC):

    @abstractmethod
    def save(self, data: List[Dict[str, Any]], filename: str) -> None:
        """
        Сохраняет данные в файл
        Args:
            data: Список словарей с данными активов
            filename: Имя файла для сохранения
        """
        pass


class JSONFormat(SaveFormat):
    def save(self, data: List[Dict[str, Any]], filename: str) -> None:

        try:
            filepath = Path(filename)
            if filepath.suffix != ".json":
                filepath = filepath.with_suffix(".json")

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"✗ Ошибка при сохранении JSON: {e}")
            raise e


class CSVFormat(SaveFormat):

    def __init__(self, delimiter: str = ",", list_separator: str = ", ") -> None:
        """
        Args:
            delimiter: Разделитель колонок CSV (по умолчанию запятая)
            list_separator: Разделитель элементов внутри списков (по умолчанию запятая с пробелом)
        """
        self.delimiter = delimiter
        self.list_separator = list_separator

    def save(self, data: List[Dict[str, Any]], filename: str) -> None:

        try:
            filepath = Path(filename)
            if filepath.suffix != ".csv":
                filepath = filepath.with_suffix(".csv")

            with open(filepath, "w", encoding="utf-8", newline="") as f:
                fieldnames = list(data[0].keys())
                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=self.delimiter
                )
                writer.writeheader()
                for item in data:
                    row = {}
                    for key, value in item.items():
                        if isinstance(value, list):
                            row[key] = self.list_separator.join(str(v) for v in value)
                        else:
                            row[key] = value
                    writer.writerow(row)

        except Exception as e:
            print(f"✗ Ошибка при сохранении CSV: {e}")
            raise e
