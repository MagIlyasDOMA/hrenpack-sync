import json
from pathlib import Path


class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent / 'config.json'
        self.encoding = 'utf-8'

    @property
    def data(self):
        return json.loads(self.config_path.read_text(self.encoding))

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        data = self.data
        data[key] = value
        self.config_path.write_text(json.dumps(data, ensure_ascii=False), encoding=self.encoding)

    def __delitem__(self, key):
        data = self.data
        del data[key]
        self.config_path.write_text(json.dumps(data, ensure_ascii=False), encoding=self.encoding)

