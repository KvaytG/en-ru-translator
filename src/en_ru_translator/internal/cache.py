import json
import logging
from pathlib import Path
from collections import defaultdict

_CURRENT_DIR = Path(__file__).parent.resolve()
_CACHE_PATH = _CURRENT_DIR.parent / "resources" / "cache.json"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TranslationCache:
    """ INTERNAL CLASS! """
    def __init__(self, max_size: int = 1024):
        self.max_size = max_size
        self.cache = {}
        self.freq = defaultdict(int)
        self._dirty = False
        self._load()

    def _load(self):
        if _CACHE_PATH.exists():
            try:
                with _CACHE_PATH.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data:
                        text = entry["text"]
                        translated = entry["translated"]
                        count = entry.get("count", 1)
                        self.cache[text] = translated
                        self.freq[text] = count
            except Exception:
                logger.warning("Failed to load cache.json, creating a new one")
        self._trim_cache()

    def _save(self):
        sorted_items = sorted(
            self.cache.items(),
            key=lambda kv: self.freq.get(kv[0], 0),
            reverse=True
        )
        data_to_save = [
            {"text": text, "translated": translated, "count": self.freq.get(text, 1)}
            for text, translated in sorted_items[:self.max_size]
        ]
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _CACHE_PATH.open("w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        self._dirty = False

    def save(self):
        if self._dirty:
            self._save()

    def _trim_cache(self):
        if len(self.cache) <= self.max_size:
            return
        to_remove = sorted(self.cache, key=lambda t: self.freq.get(t, 0))[:len(self.cache) - self.max_size]
        for text in to_remove:
            del self.cache[text]
            del self.freq[text]

    def get(self, text: str):
        if text in self.cache:
            self.freq[text] += 1
            self._dirty = True
            return self.cache[text]
        return None

    def set(self, items: list[tuple[str, str]]):
        for text, translated_text in items:
            if text not in self.cache and len(self.cache) >= self.max_size:
                self._trim_cache()
            self.cache[text] = translated_text
            self.freq[text] += 1
            self._dirty = True
