import json
from pathlib import Path
from typing import Any


class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent / 'config.json'
        self.encoding = 'utf-8'

        # Создаем файл конфигурации если его нет
        if not self.config_path.exists():
            self.config_path.write_text(json.dumps({
                "directory": "hrenpack_source",
                "managers": []
            }, ensure_ascii=False, indent=2), encoding=self.encoding)

    @property
    def data(self) -> dict:
        """Загружает и возвращает данные конфигурации"""
        try:
            return json.loads(self.config_path.read_text(self.encoding))
        except json.JSONDecodeError:
            # Если файл поврежден, создаем новый
            default_data = {"directory": "hrenpack_source", "managers": []}
            self.config_path.write_text(json.dumps(default_data, ensure_ascii=False, indent=2), encoding=self.encoding)
            return default_data

    def get(self, key: str, default: Any = None) -> Any:
        """Безопасно получает значение по ключу"""
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Получает значение по ключу (возбуждает KeyError если ключ отсутствует)"""
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Устанавливает значение и сохраняет в файл"""
        data = self.data
        data[key] = value
        self.config_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding=self.encoding
        )

    def __delitem__(self, key: str) -> None:
        """Удаляет ключ и сохраняет в файл"""
        data = self.data
        if key in data:
            del data[key]
            self.config_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding=self.encoding
            )