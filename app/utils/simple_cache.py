import hashlib

class SimpleCache:
    def __init__(self):
        self.store = {}

    def _key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def get(self, text: str):
        return self.store.get(self._key(text))

    def set(self, text: str, value):
        self.store[self._key(text)] = value
